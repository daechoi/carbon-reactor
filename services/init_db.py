import psycopg2


"""

CREATE TABLE public.staging_naked (
	id int NOT NULL GENERATED ALWAYS AS IDENTITY,
	"action" varchar NULL,
	symbol varchar NULL,
	expiration varchar NULL,
	put_call varchar NULL,
	strike float4 NULL,
	pop float4 NULL,
	credit float4 NULL,
	maxloss float4 NULL,
	created date NULL,
	inserted timestamp(0) NOT NULL DEFAULT now()
);
"""


