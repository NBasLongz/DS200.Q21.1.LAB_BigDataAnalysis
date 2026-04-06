
-- BÀI 5: TOP 5 TỪ LIÊN QUAN NHẤT THEO CATEGORY

bai1 = LOAD 'Output/BaiTap1' USING PigStorage('\t') 
       AS (id:int, word:chararray, category:chararray, aspect:chararray, sentiment:chararray);

aw_g   = GROUP bai1 BY (category, word);
aw_c   = FOREACH aw_g GENERATE FLATTEN(group) AS (category, word), COUNT(bai1) AS freq;
aw_cat = GROUP aw_c BY category;
aw_top5 = FOREACH aw_cat {
    s = ORDER aw_c BY freq DESC;
    t = LIMIT s 5;
    GENERATE FLATTEN(t);
};

STORE aw_top5 INTO 'Output/BaiTap5_Top5_Related' USING PigStorage('\t');

