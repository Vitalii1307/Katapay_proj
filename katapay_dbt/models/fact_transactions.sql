SELECT
    event_id,
    event_type,
    timestamp,
    user_id,
    provider_id,
    amount,
    currency
FROM public.raw_transactions
WHERE event_type IN ('authorization', 'settlement')