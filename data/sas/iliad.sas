

filename  homer4sa '../homer.gexf';
filename  SXLEMAP 'iliad.map';
libname   homer4sa xmlv2 xmlmap=SXLEMAP access=READONLY;

libname out ".";



DATA out.node; SET homer4sa.node; run;
DATA out.edge; SET homer4sa.edge; run;


ods tagsets.excelxp file="iliad.xls" ;                                                                                                                                           
                                                                                                                                                                                  
proc print data=out.edge noobs;
   var source  / style(data)={tagattr="format:@"};     
    var target  / style(data)={tagattr="format:@"};  
                                                                                                                                                                                                                                                                                                           
run;                                                                                                                                                                              
                                                                                                                                                                                  
ods tagsets.excelxp close;
      


















ods csv file="iliad.csv";
proc print data=edge;
run;
ods csv close;


ods csv file="C:\Users\jhu\Google Drive\technology\HOW\pydata2016\networkX\homer\data\sas\iliad.csv" options(prepend_equals="yes" 
                                   quote_by_type="yes");                                                           
                                                                                                                                        
proc print data=edge;                                                                                                                    
run;                                                                                                                                    
                                                                                                                                        
ods csv close;  







libname _a "C:\Users\jhu\Google Drive\technology\HOW\pydata2016\networkX\homer\data\sas";

%ds2csv (data=_a.edge, runmode=b, csvfile=%str(C:\Users\jhu\Google Drive\technology\HOW\pydata2016\networkX\homer\data\sas\iliad.csv));

