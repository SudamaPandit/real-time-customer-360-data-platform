{{ config(materialized='table') }}

select
    customer_id,
    count(*) as event_count,
    max(event_ts) as last_event_ts,
    sum(case when event_type = 'purchase' then 1 else 0 end) as purchase_count,
    sum(case when event_type = 'login' then 1 else 0 end) as login_count
from {{ source('silver', 'customer_events') }}
group by customer_id
