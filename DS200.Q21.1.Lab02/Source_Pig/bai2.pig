raw = LOAD 'Data/hotel-review.csv' USING PigStorage(';') AS (
    id:int, 
    review:chararray, 
    category:chararray, 
    aspect:chararray, 
    sentiment:chararray);
bai1 = LOAD 'Output/BaiTap1' USING PigStorage('\t') AS (
    id:int, 
    word:chararray, 
    category:chararray, 
    aspect:chararray, 
    sentiment:chararray);

-- 2a. Thống kê từ xuất hiện > 500 lần
grp_word = GROUP bai1 BY word;
word_freq = FOREACH grp_word GENERATE group AS word, COUNT(bai1) AS freq;
STORE (ORDER (FILTER word_freq BY freq > 500) BY freq DESC) INTO 'Output/BaiTap2_WordFreq' USING PigStorage('\t');

-- 2b. Thống kê theo Category
grp_cat = GROUP raw BY category;
cat_count = FOREACH grp_cat GENERATE group AS category, COUNT(raw) AS freq;
STORE (ORDER cat_count BY freq DESC) INTO 'Output/BaiTap2_Category' USING PigStorage('\t');

-- 2c. Thống kê theo Aspect
grp_asp = GROUP raw BY aspect;
asp_count = FOREACH grp_asp GENERATE group AS aspect, COUNT(raw) AS freq;
STORE (ORDER asp_count BY freq DESC) INTO 'Output/BaiTap2_Aspect' USING PigStorage('\t');
