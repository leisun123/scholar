CREATE EXTENSION pg_trgm;
CREATE INDEX on articles USING GIN (authors gin_trgm_ops);
CREATE INDEX on articles USING GIST (authors gist_trgm_ops);

select authors, similarity(authors, 'Jerry') as dist  from articles where authors ~ 'Jerry' order by dist desc