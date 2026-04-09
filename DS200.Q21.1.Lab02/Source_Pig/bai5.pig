
data = LOAD 'Output/BaiTap1' USING PigStorage('\t') 
AS (id:int, word:chararray, category:chararray, aspect:chararray, sentiment:chararray);

-- Đếm tần số theo (category, word)
grp = GROUP data BY (category, word);

cnt = FOREACH grp GENERATE 
    FLATTEN(group) AS (category, word),
    COUNT(data) AS freq;

-- Nhóm theo category
grp_cat = GROUP cnt BY category;

-- Lấy top 5 mỗi category
top5 = FOREACH grp_cat {
    sorted = ORDER cnt BY freq DESC;
    top = LIMIT sorted 5;
    GENERATE group AS category, FLATTEN(top);
};

STORE top5 INTO 'Output/BaiTap5' USING PigStorage('\t');
