import CreatSmall as CS
import CreatCE as CCE
import CreatAlign as CA
import CreatLableData as CLD


def MainCreat():
    CS.wmt2018_to_rawsmall('wmt2018.zh2en-Registry', 100)
    CCE.creat_cn_en()
    CA.main_creat()
    CLD.CreatLableData()


if __name__ == '__main__':
    MainCreat()