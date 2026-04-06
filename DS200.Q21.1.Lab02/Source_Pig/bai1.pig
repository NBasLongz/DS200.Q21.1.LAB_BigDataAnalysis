
raw = LOAD 'Data/hotel-review.csv' 
USING PigStorage(';') 
AS (id:int, review:chararray, category:chararray, aspect:chararray, sentiment:chararray);

clean = FOREACH raw GENERATE 
    id,
    LOWER(review) AS review,
    category,
    aspect,
    sentiment;

words = FOREACH clean GENERATE 
    id,
    FLATTEN(TOKENIZE(review)) AS word,
    category,
    aspect,
    sentiment;

filtered = FILTER words BY word IS NOT NULL;

STORE filtered INTO 'Output/BaiTap1' USING PigStorage('\t');
