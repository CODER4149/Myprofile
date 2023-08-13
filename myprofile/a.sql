  select * from
                            (select c.store_code,
                                    case when p.bill_cnt is not null then  p.bill_cnt else 0 end as bills_count,
                             ((d.avg_amount_hole) / 100000)::numeric(10, 2)                             as avg_amount_hole,
                                c.site_short_name                                                          as site_name,
                                c.city,
                                c.updated_at,
                                r.panel_no,


--     average amount Today sale average
                   case when c.avg_amount is not null then (c.avg_amount)::integer else 0 end as avg_amount,
                   b.round,
                   case
                       when c.today_hike is not null  then round(c.today_hike)
                       when c.today_hike is null then 0
                   end                     as Today_hike,
--     FLOOR((c.today_amt/(c.today_amt/b.round )::numeric(10,2) )*100)
--     as sale_diff_percentage ,
                    case
                        when
                            b.round!=0 and (c.today_amt / b.round) != 0
                        then
                            FLOOR((c.today_amt / (c.today_amt / b.round)::numeric(10, 2)) * 100)  else 0
                    end  as sale_diff_percentage,
                    case when c.today_amt is not null then c.today_amt else 0 end           as current_sale,
                    case
                       when
                           b.round != 0 and b.round is not null
            --              d.avg_amount_hole is the hole previous mondays average
                           and (c.today_amt / b.round)::numeric(10, 2) > 0
                            or d.avg_amount_hole is null
                        then
            --                this is current day prediction when sale is greater than 0

                           (c.today_amt / b.round)::numeric(10, 2)

                       else
 --       this is when todays predicted sale is  0 or null

                           ((d.avg_amount_hole) / 100000)::numeric(10, 2)
                    end                            as predicted_sale,

 --      This is today current time predicted sale
                   case
                       when
                           b.round != 0
                       then
                           (c.today_amt / b.round)::numeric(10, 2)
                       else 0
                       end                         as predicted_sale_current_time,
                   w.this_week_amt                                                            as this_week_amt,
                   case when w.today_qty is not null then w.today_qty else 0 end as unit_qty

                    from (
 --       Query for returning predicted value current datetime
                             select case
                                        when
                                            round(avg(slot_percent), 2) is not null and round(avg(slot_percent), 2) != 0 then round(avg(slot_percent), 2)
                                        else 0
                                        end as round,
                             store_code
                                     from (select round(total_slot
                                                / round(avg(slot_percent) over (partition by day_type, store_code), 3), 1) as predicted,

                                      abs(round(((day_total
                                          - round(total_slot / round(avg(slot_percent) over (partition by day_type, store_code), 3), 1))
                                          / day_total), 2) *
                                          100)                                                                             as error_percent,
                                      *
                                           from (select case when total_slot!= 0 then (total_slot / (sum(total_slot) over (partition by date_, store_code))) else 0 end as slot_percent,
                                                        slot,
                                                        store_code,
                                                        date_,
                                                        total_slot,
                                                        sum(total_slot) over (partition by date_, store_code)                  as day_total,
                                                        case
                                                            when date_part('isodow', date_) in (6, 7) then 'Weekend'
                                                            else 'Weekday'
                                                            end                                                                as day_type
                                             from (select sum(amt) as total_slot,
                                                          slot,
                                                          store_code,
                                                          b.date_
                                                   from (select a.*,
                                                                case
                                                                    when a.hour >= 7 and
                                                                         a.hour < EXTRACT(hour FROM (current_time + interval '330 mins'))
                                                                        then 'Morning'
                                                                    when a.hour >= EXTRACT(hour FROM (current_time + interval '330 mins')) and
                                                                         a.hour <= 23 then 'Evening'
                                                                    end as slot
                                                             from (select sum(amount)                  as amt,
                                                                          date_part('hour', bill_time) as hour,
                                                                          date(bill_time)                 date_,
                                                                          store_code
                                                                   from sales_txn
                                                                   group by date_part('hour', bill_time),
                                                                            date(bill_time), store_code) as a) as b
                                                               group by slot, store_code, date_) as c) as d
                                                   where slot = 'Morning') as e
                                             group by store_code) b
                                     Right join
                                     (
                                --                     Query for returning store_code,today_hike
                                          select sm.site_short_name,
                                                 sm.city,
                                                sdl.store_code,
                                                sdl.updated_at,
                                                sdl.site_name,
                                --                             avg_amount,
                                --                             sdl.today_amt,
                                --                             ((1.0 - sdl.today_amt*100000.0 / avg_amount) * 100) * -1.0 as today_hike


                                                case
                                                    when
                                                            avg_amount is not null and avg_amount != 0 then avg_amount
                                                    else 0
                                                        end as avg_amount,
                                            case
                            --                             coalesce(sdl.today_amt != 0, 1) as today_amt,
                                                when
                                                    sdl.today_amt is not null and sdl.today_amt != 0 then sdl.today_amt
                                                else 0
                                                end as today_amt,
                            --                             sdl.today_amt,
                                            case
                                                when
                                                       avg_amount != 0
                                                    then ((1.0 - sdl.today_amt * 100000.0 / avg_amount) * 100) * -1.0
                                                else 0
                                                end as today_hike
                                                         from sales_data_live sdl
                                                                  left join (select a.store_code,
                                                                                    avg(amount) as avg_amount
                                                                             from (select sum(amount)                          as amount,
                                                                                          date(bill_time),
                                                                                          store_code,
                                                                                          EXTRACT(ISODOW FROM date(bill_time)) as weekday
                                                                                   from sales_txn
                                                                                   where bill_time::time < current_time + interval '330 mins'
                                                                                   group by date(bill_time), store_code
                                                                                   having EXTRACT(ISODOW FROM date(bill_time)) = EXTRACT(ISODOW FROM CURRENT_DATE)) a
                                                                             group by store_code) b
                                                                            on sdl.store_code = b.store_code
                                                                  join store_master sm on sdl.store_code = sm.site_code

                                                         where sm.org_code = 'SU') c
                                                     on b.store_code = c.store_code
                                         Right join
                                             (
                                        --                        Query for  returns this_week_amt
                                                 select sm.site_name,
                                                        --           count(st.bill_no) as bills_qty,
                                                        sum(st.amount)    as current_sale,
                                                        sdl.today_qty,
                                                        date(sdl.updated_at),
                                                        sdl.store_code,
                                                        sdl.this_week_amt as this_week_amt,
                                                        sm.site_short_name
                                                 from sales_txn st
                                                       right   join
                                                      store_master sm
                                                      on
                                                          st.store_code = sm.site_code
                                                         right join
                                                      sales_data_live sdl
                                                      on sm.site_name = sdl.site_name
                                                 where date(sdl.updated_at) = current_date
                                                   and sm.org_code = 'SU'
                                                 group by date(sdl.updated_at), sm.site_name, sdl.this_week_amt, sdl.store_code, sdl.today_qty,sm.site_short_name) w
                                             on w.store_code = c.store_code
                                        left join (select count(bill_no) as  bill_cnt ,store_code from sales_txn where date(bill_time) = current_date
                                              group by store_code) p on
                                            p.store_code=w.store_code
                                        left join

    --       Query for when predicted sale is 0 then query returns all previous mondays average
                                                    (select   a.store_code,
                                                            avg(amount) as avg_amount_hole
                                                                    from (
                                                                                select sum(amount)                          as amount,
                                                                               date(bill_time),
                                                                                store_code,
                                                                                 EXTRACT(ISODOW FROM date(bill_time)) as weekday
                                                                                from sales_txn
                                            --                                          where bill_time::time < current_time + interval '330 mins'
                                                                                        group by date(bill_time), store_code
                                                                                        having EXTRACT(ISODOW FROM date(bill_time)) = EXTRACT(ISODOW FROM CURRENT_DATE)) a
                                                                            group by store_code) d
                                                on w.store_code = d.store_code
                                                    left join
                                                                    (select panel_no, site_code
                                                                                 from panel_store_mapping) r
                                                    on r.site_code = d.store_code
                                                    ) a
                                            where   a.site_name is not null
                                                group by a.store_code, a.panel_no, a.site_name, a.avg_amount_hole, a.avg_amount, a.round, a.today_hike,a.unit_qty,a.city,
                                                                                 a.updated_at,a.sale_diff_percentage, a.current_sale,a.bills_count, a.predicted_sale_current_time, a.predicted_sale, a.this_week_amt
    