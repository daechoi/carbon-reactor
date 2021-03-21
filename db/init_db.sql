
-- public.staging_credit_spreads definition

-- Drop table

-- DROP TABLE public.staging_credit_spreads;

CREATE TABLE public.staging_credit_spreads (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	txn varchar NULL,
	symbol varchar NULL,
	expiration varchar NULL,
	put_call varchar NULL,
	short_strike float4 NULL,
	long_strike float4 NULL,
	initial_stock_price float4 NULL,
	pop float4 NULL,
	credit float4 NULL,
	maxloss float4 NULL,
	created date NULL,
	inserted timestamp(0) NOT NULL DEFAULT now(),
	link varchar NULL,
	CONSTRAINT staging_credit_spreads_pk PRIMARY KEY (id),
	CONSTRAINT staging_credit_spreads_un UNIQUE (txn, symbol, expiration, put_call, short_strike, long_strike, initial_stock_price, pop, credit, maxloss)
);


-- public.staging_long_calls_puts definition

-- Drop table

-- DROP TABLE public.staging_long_calls_puts;

CREATE TABLE public.staging_long_calls_puts (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	txn varchar NOT NULL,
	symbol varchar NULL,
	company_name varchar NULL,
	avg_daily_call_vol int8 NULL,
	current_call_open_int int8 NULL,
	inserted timestamp(0) NOT NULL DEFAULT now(),
	site_updated timestamp(0) NULL,
	CONSTRAINT staging_long_calls_puts_pk PRIMARY KEY (id),
	CONSTRAINT staging_long_calls_puts_un UNIQUE (txn, symbol, company_name, avg_daily_call_vol, current_call_open_int)
);

-- public.staging_naked definition

-- Drop table

-- DROP TABLE public.staging_naked;

CREATE TABLE public.staging_naked (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	txn varchar NULL,
	symbol varchar NULL,
	expiration varchar NULL,
	put_call varchar NULL,
	strike float4 NULL,
	pop float4 NULL,
	credit float4 NULL,
	maxloss float4 NULL,
	created date NULL,
	inserted timestamp(0) NOT NULL DEFAULT now(),
	link varchar NULL,
	CONSTRAINT staging_naked_pk PRIMARY KEY (id),
	CONSTRAINT staging_naked_un UNIQUE (txn, symbol, expiration, put_call, strike, pop, credit, maxloss)
);

