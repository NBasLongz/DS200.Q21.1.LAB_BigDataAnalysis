raw = LOAD 'Data/hotel-review.csv' USING PigStorage(';') 
AS (id:int, review:chararray, category:chararray, aspect:chararray, sentiment:chararray);

clean = FOREACH raw GENERATE 
    id,
    review,
    category,
    aspect,
    LOWER(TRIM(REPLACE(sentiment, '\\r|\\n', ''))) AS sentiment;

-- NEGATIVE
neg = FILTER clean BY sentiment == 'negative';
grp_neg = GROUP neg BY aspect;
cnt_neg = FOREACH grp_neg GENERATE group AS aspect, COUNT(neg) AS total;
sorted_neg = ORDER cnt_neg BY total DESC;

STORE sorted_neg INTO 'Output/BaiTap3_NegativeAll' USING PigStorage('\t');

-- POSITIVE
pos = FILTER clean BY sentiment == 'positive';
grp_pos = GROUP pos BY aspect;
cnt_pos = FOREACH grp_pos GENERATE group AS aspect, COUNT(pos) AS total;
sorted_pos = ORDER cnt_pos BY total DESC;

STORE sorted_pos INTO 'Output/BaiTap3_PositiveAll' USING PigStorage('\t');
