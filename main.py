import CreatSmall as CS
import CreatCE as CCE
import CreatAlign as main
if __name__ == "__main__":
    CS.wmt2018_to_rawsmall('wmt2018.zh2en-Registry', 100)
    CCE.creat_cn_en()
    main.main_creat()