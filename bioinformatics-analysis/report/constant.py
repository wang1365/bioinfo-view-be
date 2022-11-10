ONTARGET = {
    "filepath": "QC/ontarget.txt",
    "type": "raw"
}

QC_TIP = {
    "filepath": "QC/QC_tip",
    "type": "raw"
}

QC = {
    "filepath": "QC/QC_info",
    "sep": "\t",
    "header": 0,
}

QN11 = {
    "filepath": "QC/QN11.depth",
    "sep": "\t",
    "header": 0,
}

QT11 = {
    "filepath": "QC/QT11.depth",
    "sep": "\t",
    "header": 0,
}

MUT_GERMLINE = {
    "filepath": "Mut_germline/QT11.combined.standard-new.csv",
    "sep": ",",
    "header": 0,
}

MUT_SOMATIC = {
    "filepath": "Mut_somatic/QN11_QT11.combined.standard-new.csv",
    "sep": ",",
    "header": 0,
}

FILE_MAPPINGS = {
    # 质控
    "QC": QC,
    "QN11": QN11,
    "QT11": QT11,
    "MUT_GERMLINE": MUT_GERMLINE,
    "MUT_SOMATIC": MUT_SOMATIC,
    "ONTARGET": ONTARGET,
    "QC_TIP": QC_TIP,

    # 突变分析

    # 融合分析
    "FUSION_QT11": {
        "filepath": "fusion_germline/QT11.fusions",
        "sep": "\t",
        "header": 0
    },
    "FUSION_QN11": {
        "filepath": "fusion_germline/QN11.fusions",
        "sep": "\t",
        "header": 0
    },
    "FUSION_QN11_SOMATIC": {
        "filepath": "fusion_somatic/QN11_QT11.somatic_fusions",
        "sep": "\t",
        "header": 0
    },

    # 拷贝数变异分析

    # 微卫星不稳定结果

    # 肿瘤突变符合分析结果

    # 同源重组缺陷分析结果
}
