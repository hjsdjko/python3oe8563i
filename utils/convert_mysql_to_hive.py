# coding: utf-8
__author__ = 'ila'

import re

import sqlparse


class ConvertMySQLToHive(object):
    def __init__(self, db_name):
        self.hive_datatype_mapping = {
            "int": "int",
            "integer": "int",
            "bigint": "int",
            "smallint": "int",
            "tinyint": "int",
            "decimal": "string",

            "char": "string",
            "varchar": "string",

            "text": "string",
            "tinytext": "string",
            "longtext": "string",
            "mediumtext": "string",

            "datetime": "string",
            "date": "string",
            "timestamp": "string",
        }

        self.db_name = db_name

    def extract_definitions(self, token_list):
        '''
        读取create table里的字段名和数据类型
        :param token_list:
        :return:
        '''
        definitions = []
        tmp = []
        par_level = 0
        for token in token_list.flatten():
            if token.is_whitespace:
                continue
            elif token.match(sqlparse.tokens.Punctuation, '('):
                par_level += 1
                continue
            if token.match(sqlparse.tokens.Punctuation, ')'):
                if par_level == 0:
                    break
                else:
                    par_level += 1
            elif token.match(sqlparse.tokens.Punctuation, ','):
                if tmp:
                    definitions.append(tmp)
                tmp = []
            else:
                tmp.append(token.value)
        if tmp:
            definitions.append(tmp)
        return definitions

    def convert_mysql_to_hive(self, raw_mysql: str) -> list:
        # 替换注释
        results = re.findall("/\*.*?\*/", raw_mysql, re.DOTALL)
        for result in results:
            raw_mysql = raw_mysql.replace(result, "")

        hive_list = []
        # 开始解析,分割成句子list
        for parsed in sqlparse.parse(raw_mysql):

            if len(parsed.value) < 1:
                continue

            # 判断句子类型
            parsed_value = parsed.value
            parsed_value = parsed_value.lower()
            parsed_value = parsed_value.replace("\n", "").replace("\r", "").replace("\r\n", "")
            if 'create' in parsed_value and "database" in parsed_value:
                method = "create database"
            elif 'drop' in parsed_value and "table" in parsed_value:
                method = "drop table"
            elif 'create' in parsed_value and "table" in parsed_value:
                method = "create table"
            elif 'insert' in parsed_value:
                method = "insert"
            else:
                method = ""

            if len(method) < 1:
                continue

            # 组装创建数据库
            if 'create database' in method:
                tokens = parsed.tokens
                for token in tokens:
                    token_value = f"{token.value}"
                    if "`" in token_value:
                        self.db_name = token_value
                        self.db_name = self.db_name.replace("`", "")

                if ';' in tokens:
                    hive_create_db_sql = " ".join([token.value for token in tokens[:-2] if len(token.value) > 1])
                else:
                    hive_create_db_sql = " ".join([token.value for token in tokens[:-1] if len(token.value) > 1])

                hive_create_db_sql = hive_create_db_sql.replace("`", "")
                hive_create_db_sql = hive_create_db_sql.lower()
                if "if not exists" not in hive_create_db_sql:
                    hive_create_db_sql = hive_create_db_sql.replace(self.db_name, f"if not exists {self.db_name}")

                if len(hive_create_db_sql) > 5:
                    hive_list.append(hive_create_db_sql)

            # 删除数据库表
            elif "drop table" in method:
                tokens = parsed.tokens
                if ';' in tokens:
                    idx2 = -2

                else:
                    idx2 = -1

                idx1 = 0
                for idx, token in enumerate(tokens[:idx2]):
                    if len(token.value) > 1 and "DROP" in token.value:
                        idx1 = idx
                        break

                table_name = ""
                for token in tokens[idx1:idx2]:
                    token_value = f"{token.value}"
                    if len(token_value) > 2 and "`" in token_value and "(" not in token_value and ")" not in token_value:
                        table_name = f"{token_value}"
                        table_name = table_name.replace("`", "")
                        break

                hive_drop_table_sql = " ".join([token.value for token in tokens[idx1:idx2]])
                if '.' not in table_name:
                    hive_drop_table_sql = hive_drop_table_sql.replace(table_name, f"{self.db_name}.{table_name}")

                hive_drop_table_sql = hive_drop_table_sql.replace("`", "")
                hive_drop_table_sql = hive_drop_table_sql.lower()
                if len(hive_drop_table_sql) > 5:
                    hive_list.append(hive_drop_table_sql)
            # 组装创建数据库表
            elif "create table" in method:
                table_name = ""
                col_list = []

                for token in parsed.tokens:
                    token_value = f"{token.value}"
                    if len(token_value) > 2 and "`" in token_value and "(" not in token_value and ")" not in token_value:
                        table_name = f"{token_value}"
                        table_name = table_name.replace("`", "")
                        break

                _, tokens = parsed.token_next_by(i=sqlparse.sql.Parenthesis)
                if tokens is None:
                    continue
                definition_list = self.extract_definitions(tokens)
                for definition in definition_list:
                    if len(definition) < 2:
                        continue
                    if 'primary' in definition[0].lower() or 'unique' in definition[0].lower():
                        continue
                    col_list.append(
                        f"{definition[0].lower()} {self.hive_datatype_mapping.get(definition[1].lower(), 'string')}")

                if '.' in table_name:
                    hive_create_table_sql = f'''create table if not exists {table_name}( {",".join(col_list)} )'''
                else:
                    hive_create_table_sql = f'''create table if not exists {self.db_name}.{table_name}( {",".join(col_list)} )'''

                hive_create_table_sql = hive_create_table_sql.replace("`", "")
                if len(hive_create_table_sql) > 5:
                    hive_list.append(hive_create_table_sql)

            # 组装数据库表记录
            if "insert" in method:
                table_name = ""
                # 处理提取table name失败的情况
                ret = re.findall(r'`(.*?)` \(', parsed.value)
                if len(ret) > 0:
                    table_name = ret[0]
                cols_string=""
                values_string = ""
                for token in parsed.tokens:
                    if token is None:
                        continue
                    token_value = f"{token.value}"
                    print("-----",token_value,"-----")
                    if table_name in token_value and "(" in token_value and ")" in token_value:
                        cols_string = f"{token_value}"
                        cols_string = cols_string.replace("`", "")
                    if "'" in token.value and "(" in token.value and ")" in token.value:
                        values_string = token_value
                        values_string = values_string.replace("VALUES", "values")



                if len(self.db_name) > 1 and '.' not in table_name:
                    hive_insert_sql = f'''insert into {self.db_name}.{cols_string} {values_string}'''
                else:
                    hive_insert_sql = f''' insert into {cols_string} {values_string}'''

                if len(hive_insert_sql) > 5:
                    hive_list.append(hive_insert_sql)

        return hive_list


if __name__ == "__main__":
    with open(r"C:\Users\Qiusw\Desktop\python8wvnk.sql", encoding="utf-8") as f:
        data = f.read()
    cv = ConvertMySQLToHive("")
    hive_list = cv.convert_mysql_to_hive(data)
    with open("hive.sql", "w", encoding="utf-8") as f:
        for l in hive_list:
            if len(l) < 5:
                continue
            f.write(l + "\n")
