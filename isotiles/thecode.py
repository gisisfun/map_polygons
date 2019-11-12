from gnaf.parameters import Tables,Defaults

import os,sqlite3,subprocess


class Process:    
    
    class Do_Stuff():
        __slots__ =("SpatialitePath","Slash")
        def __init__(self,splitePath):
            self.SpatialitePath = splitePath
            my_os = str(os.name)
            #print(my_os)
            #ntValues = OSVars.nt()
            #posixValues = OSVars.posix()
            #offValues = Offsets()
        
            if (my_os is 'posix'):
                self.Slash = '/' # posixValues.Slash # '/'
            else:
                self.Slash = '\\'# ntValues.Slash # '\\'
        

        
        def sql_to_db (self,sqltext, db):
            '''
            source: https://stackoverflow.com/questions/44557745/build-sqlite-query-in-python-but-execute-it-using-sqlite3-command-line-program            '''
            thesql  = str(sqltext)
            
            subprocess.check_output(
                ["sqlite3",
                 "{Splite}{slash}{db}.sqlite".\
                 format(db = db,\
                        slash = self.Slash,\
                        Splite = self.SpatialitePath)], input=bytes(thesql.encode("utf-8")))
            

    
    class Collect:
        def __init__(self,gnaf_path,sub_dir):
            self.GNAFPath = gnaf_path
            self.subDir = sub_dir
            #print('hello there')

        def pipes_to_comma(self,thefile):
            '''\
            Read a lines from a file line by line into an output file.
            Replace all '|' characters with a ','.
            '''
            srcfile = self.GNAFPath + self.subDir + thefile + '.psv'
            destfile = self.GNAFPath + self.subDir + thefile + '.csv'
            outfile = open(str(destfile), 'w')
            with open(srcfile, 'r', encoding='utf-8') as infile:
                for line in infile:
                    newline = line.replace('|',',')
                    outfile.write(newline)

            outfile.close()
            
        def state_pipes(self,tbl):
            for thestate in tbl.stateList:
                self.pipes_to_comma(tbl.filePiped.format(state = thestate))

        def drop_inp_sql_st(self, tblexp, theState):
            #d = Defaults()
            Def = Defaults()
            expText = tblexp.format(state = theState)
            return expText

        def drop_states_sql_st(self, tbl):
            #d = Defaults()
            Def = Defaults()
            expText =''
            for theState in tbl.stateList:
                expText = expText + self.drop_inp_sql_st(tbl.sqlDropInpTbl,theState) + '\n'
            return expText

        def load_sql_st(self, tblname, theState):
            #d = Defaults()
            Def = Defaults()
            newState = tblname
            if theState is not '':
                newState = tblname.format(state = theState)
            
            expText = Def.sqlLoad.format(table = newState, subdir = self.subDir, filespath = self.GNAFPath) + '\n'
            
            return expText

        def load_states_sql_st(self, tbl):
            #d = Defaults()
            Def = Defaults()
            expText = ""
            for theState in tbl.stateList:
                expText = expText + self.load_sql_st(tbl.filePiped,theState)
            
            return expText
                
    class Collate:

        def create_merge_standard_sql_st(tbl,gnafPath,subDir):
            print(tbl.filePiped)
            c = Process.Collect(gnafPath,subDir)
            c.state_pipes(tbl)
            expText = c.drop_states_sql_st(tbl)
            
            expText = expText + c.load_states_sql_st(tbl)
            
            expText = expText + tbl.sqlDropMrgTbl
            expText = expText + tbl.sqlDropOutTbl
            
            sqlText = '\n' + tbl.sqlStart +'\n'
            
            for thestate in tbl.stateList:
                sqlText = sqlText + tbl.sqlState.format(state = thestate)
                if thestate is not tbl.stateList[-1]:
                    sqlText = sqlText + '\nUNION\n'
                else:
                    sqlText = sqlText + ';\n'
            expText = expText + '\n' + sqlText 
            expText = expText + '\n'+ tbl.sqlTable 
            expText = expText + '\n' + tbl.sqlInsert
            expText = expText + '\n' + tbl.sqlDropMrgTbl
            expText = expText + '\n' + c.drop_states_sql_st(tbl)
            expText = expText + '\nVACUUM;\n'
            
            return expText
        
        def create_merge_auth_sql_st(tbl,gnafPath,subDir):
            print(tbl.filePiped)
            c = Process.Collect(gnafPath,subDir)
            c.pipes_to_comma(tbl.filePiped)
            expText = tbl.sqlDropInpTbl + '\n'
            expText = expText + c.load_sql_st(tbl.filePiped, '') + '\n'
            expText = expText + tbl.sqlDropOutTbl + '\n'
            expText = expText + tbl.sqlTable + '\n'
            expText = expText + tbl.sqlInsert + '\n'
            expText = expText + tbl.sqlDropInpTbl + '\n'
            return expText

        def create_views_sql_st(tbl):
            print(tbl.filePiped)
            
            expText = tbl.sqlDropOutTbl + '\n'
            expText = expText + tbl.sqlView 
            return expText
        
        def create_foreign_keys_sql_st(tbl):
            print('Foreign Keys')
            
            expText = tbl.sqlConstraints  
            return expText