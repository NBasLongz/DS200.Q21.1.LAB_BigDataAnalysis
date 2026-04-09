data = LOAD 'Output/BaiTap1' USING PigStorage('\t') 
AS (id:int, word:chararray, category:chararray, aspect:chararray, sentiment:chararray);

-- POSITIVE
pos = FILTER data BY sentiment == 'positive';

grp_pos = GROUP pos BY (category, word);
cnt_pos = FOREACH grp_pos GENERATE 
    FLATTEN(group) AS (category, word), 
    COUNT(pos) AS freq;

grp_cat_pos = GROUP cnt_pos BY category;

top_pos = FOREACH grp_cat_pos {
    sorted = ORDER cnt_pos BY freq DESC;
    top5 = LIMIT sorted 5;
    GENERATE group AS category, FLATTEN(top5);
};

STORE top_pos INTO 'Output/BaiTap4_Positive' USING PigStorage('\t');


-- NEGATIVE
neg = FILTER data BY sentiment == 'negative';

grp_neg = GROUP neg BY (category, word);
cnt_neg = FOREACH grp_neg GENERATE 
    FLATTEN(group) AS (category, word), 
    COUNT(neg) AS freq;

grp_cat_neg = GROUP cnt_neg BY category;

top_neg = FOREACH grp_cat_neg {
    sorted = ORDER cnt_neg BY freq DESC;
    top5 = LIMIT sorted 5;
    GENERATE group AS category, FLATTEN(top5);
};

STORE top_neg INTO 'Output/BaiTap4_Negative' USING PigStorage('\t');
