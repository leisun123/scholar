CREATE EXTENSION pg_trgm;
CREATE INDEX on articles USING GIN (authors gin_trgm_ops);
CREATE INDEX on articles USING GIST (authors gist_trgm_ops);

select authors, similarity(authors, 'Jerry') as dist  from articles where authors ~ 'Jerry' order by dist；


 create table articles_count(col int);

 insert into articles_count ( select count(*) from articles);

CREATE OR REPLACE FUNCTION articles_insert_func()  RETURNS TRIGGER AS $$
        BEGIN
                update  articles_count  set col = col + 1;
                RETURN null;
        END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION articles_delete_func()  RETURNS TRIGGER AS $$
        BEGIN
                update articles_count set col = col - 1;
                RETURN null;
        END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER articles_insert
    AFTER INSERT ON articles
    FOR EACH ROW
    EXECUTE PROCEDURE articles_insert_func();

CREATE TRIGGER articles_delete
    AFTER DELETE ON articles
    FOR EACH ROW
    EXECUTE PROCEDURE articles_delete_func()


