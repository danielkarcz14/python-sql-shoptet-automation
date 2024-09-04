update suroviny
set mnozstvi = 500
where merna_jednotka = 'ks';

update suroviny
set mnozstvi = 2000
where merna_jednotka = 'kg';

update suroviny
set mnozstvi = 200
where merna_jednotka = 'kg' and kod_suroviny IN ('1001_H1', '9005_H1');