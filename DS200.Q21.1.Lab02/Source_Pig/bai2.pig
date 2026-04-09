raw = LOAD 'Data/hotel-review.csv' USING PigStorage(';') 
AS (id:int, review:chararray, category:chararray, aspect:chararray, sentiment:chararray);

bai1 = LOAD 'Output/BaiTap1' USING PigStorage('\t') 
AS (id:int, word:chararray, category:chararray, aspect:chararray, sentiment:chararray);

-- 2a. WORD FREQ > 500
grp_word = GROUP bai1 BY word;
word_freq = FOREACH grp_word GENERATE group AS word, COUNT(bai1) AS freq;
word_filtered = FILTER word_freq BY freq > 500;
STORE (ORDER word_filtered BY freq DESC) INTO 'Output/BaiTap2_WordFreq' USING PigStorage('\t');

-- 2b. CATEGORY COUNT
grp_cat = GROUP raw BY category;
cat_count = FOREACH grp_cat GENERATE group AS category, COUNT(raw) AS total;
STORE (ORDER cat_count BY total DESC) INTO 'Output/BaiTap2_Category' USING PigStorage('\t');

-- 2c. ASPECT COUNT
grp_asp = GROUP raw BY aspect;
asp_count = FOREACH grp_asp GENERATE group AS aspect, COUNT(raw) AS total;
STORE (ORDER asp_count BY total DESC) INTO 'Output/BaiTap2_Aspect' USING PigStorage('\t');
