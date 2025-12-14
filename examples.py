"""
文献整理工具使用示例
演示如何使用文献分析API
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:8000"


def analyze_text_example():
    """分析文献文本示例"""
    print("\n" + "="*60)
    print("示例1: 分析临床研究文本")
    print("="*60)

    clinical_text = """
    Background: Hypertension is a major risk factor for cardiovascular disease.
    This randomized controlled trial evaluated the efficacy of a new angiotensin
    receptor blocker (ARB) in patients with stage 2 hypertension.

    Objective: To determine whether the new ARB is superior to placebo in reducing
    systolic blood pressure in patients with stage 2 hypertension.

    Methods: We conducted a double-blind, placebo-controlled trial involving
    200 patients aged 18-65 years with stage 2 hypertension. Patients were
    randomized to receive either the new ARB (n=100) or placebo (n=100) for
    12 weeks. The primary outcome was change in systolic blood pressure from
    baseline to week 12.

    Results: The treatment group showed a significant reduction in systolic
    blood pressure compared to placebo (mean difference -15.2 mmHg, 95% CI
    -18.5 to -11.9, p<0.001). The drug was well tolerated with no serious
    adverse events.

    Conclusion: The new ARB is effective and well-tolerated for the treatment
    of stage 2 hypertension.
    """

    data = {
        "text": clinical_text,
        "title": "Efficacy of New ARB in Stage 2 Hypertension"
    }

    try:
        response = requests.post(f"{BASE_URL}/analyze/text", json=data, timeout=30)
        result = response.json()

        print(f"\n文献类型: {result['paper_type_description']}")
        print(f"置信度: {result['confidence']:.2%}")
        print(f"\n结构化信息:")
        print(f"  - 研究背景: {result['core_info']['background'][:100]}...")
        print(f"  - 研究目的: {result['core_info']['objective'][:100]}...")
        print(f"  - 研究方法: {result['core_info']['methods'][:100]}...")
        print(f"  - 研究结果: {result['core_info']['results'][:100]}...")
        print(f"  - 结论: {result['core_info']['conclusion'][:100]}...")

    except Exception as e:
        print(f"错误: {e}")


def analyze_case_report_example():
    """分析病例报告示例"""
    print("\n" + "="*60)
    print("示例2: 分析病例报告")
    print("="*60)

    case_text = """
    Case Report: Acute Myocardial Infarction in a Young Woman

    Case Presentation: A 32-year-old female patient presented to the emergency
    department with severe chest pain and dyspnea. The patient had no previous
    history of coronary artery disease but had a family history of premature
    coronary artery disease. On physical examination, she was anxious and
    diaphoretic with a blood pressure of 90/60 mmHg and heart rate of 110 bpm.

    Clinical Examination: ECG showed ST-segment elevation in leads II, III, and
    aVF consistent with inferior wall myocardial infarction. Cardiac biomarkers
    were significantly elevated (troponin I: 15.2 ng/mL). Echocardiography
    revealed reduced left ventricular function with inferior wall hypokinesis.

    Diagnosis: Acute inferior wall myocardial infarction was diagnosed based on
    clinical presentation, ECG changes, and elevated cardiac biomarkers.
    Coronary angiography revealed 100% occlusion of the right coronary artery.

    Treatment: The patient underwent emergent percutaneous coronary intervention
    (PCI) with drug-eluting stent placement. She was started on dual antiplatelet
    therapy (aspirin and clopidogrel), beta-blocker, ACE inhibitor, and statin.

    Outcome: The patient recovered well post-procedure. Follow-up echocardiography
    at 3 months showed improved left ventricular function. She remained asymptomatic
    at 6-month follow-up.
    """

    data = {
        "text": case_text,
        "title": "Acute MI in Young Woman - Case Report"
    }

    try:
        response = requests.post(f"{BASE_URL}/analyze/text", json=data, timeout=30)
        result = response.json()

        print(f"\n文献类型: {result['paper_type_description']}")
        print(f"置信度: {result['confidence']:.2%}")
        print(f"\n结构化信息:")
        print(f"  - 病例概述: {result['core_info']['case_summary'][:100]}...")
        print(f"  - 临床表现: {result['core_info']['clinical_presentation'][:100]}...")
        print(f"  - 诊断过程: {result['core_info']['diagnosis'][:100]}...")
        print(f"  - 治疗方案: {result['core_info']['treatment'][:100]}...")
        print(f"  - 治疗结果: {result['core_info']['outcome'][:100]}...")

    except Exception as e:
        print(f"错误: {e}")


def analyze_basic_research_example():
    """分析基础研究示例"""
    print("\n" + "="*60)
    print("示例3: 分析基础研究")
    print("="*60)

    basic_text = """
    Background: The molecular mechanisms underlying tumor suppressor p53
    regulation remain incompletely understood. Recent studies suggest that
    non-coding RNAs play important roles in p53-mediated transcriptional
    control.

    Objective: To investigate the role of microRNA-34a (miR-34a) in p53
    regulation and its impact on cancer cell proliferation.

    Methods: We performed cell culture experiments using human lung cancer
    cell lines (A549 and H1299). Western blot analysis was used to detect
    protein expression. Real-time PCR was used to measure mRNA levels.
    Cell proliferation was assessed using MTT assay. Luciferase reporter
    assays were performed to confirm target binding.

    Results: miR-34a expression was significantly downregulated in lung
    cancer tissues compared to adjacent normal tissues (p<0.01). Overexpression
    of miR-34a in A549 cells resulted in decreased cell proliferation
    (p<0.001) and increased apoptosis (p<0.01). miR-34a directly targeted
    the 3'UTR of SIRT1 mRNA and suppressed its expression. Mechanistically,
    miR-34a-mediated SIRT1 downregulation led to increased acetylation of
    p53 and activation of p53-dependent apoptotic pathways.

    Conclusion: miR-34a acts as a tumor suppressor by targeting SIRT1 and
    activating p53-mediated apoptosis. These findings suggest that miR-34a
    could be a potential therapeutic target for lung cancer treatment.
    """

    data = {
        "text": basic_text,
        "title": "miR-34a Regulates p53 via SIRT1 Targeting"
    }

    try:
        response = requests.post(f"{BASE_URL}/analyze/text", json=data, timeout=30)
        result = response.json()

        print(f"\n文献类型: {result['paper_type_description']}")
        print(f"置信度: {result['confidence']:.2%}")
        print(f"\n结构化信息:")
        print(f"  - 科学问题: {result['core_info']['scientific_question'][:100]}...")
        print(f"  - 研究方法: {result['core_info']['research_method'][:100]}...")
        print(f"  - 研究结果: {result['core_info']['results'][:100]}...")
        print(f"  - 研究结论: {result['core_info']['conclusion'][:100]}...")
        print(f"  - 作用机制: {result['core_info']['mechanism'][:100]}...")

    except Exception as e:
        print(f"错误: {e}")


def analyze_doi_example():
    """通过DOI分析示例"""
    print("\n" + "="*60)
    print("示例4: 通过DOI分析文献")
    print("="*60)

    # 示例DOI（可能需要替换为实际可访问的DOI）
    doi = "10.1371/journal.pone.0123456"

    data = {"doi": doi}

    try:
        print(f"正在分析DOI: {doi}")
        response = requests.post(f"{BASE_URL}/analyze/doi", json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            print(f"\n文献类型: {result['paper_type_description']}")
            print(f"置信度: {result['confidence']:.2%}")

            if 'metadata' in result['full_analysis']:
                metadata = result['full_analysis']['metadata']
                print(f"\n文献信息:")
                print(f"  - 标题: {metadata.get('title', 'N/A')}")
                print(f"  - 作者: {', '.join(metadata.get('authors', [])[:3])}...")
                print(f"  - 期刊: {metadata.get('journal', 'N/A')}")
                print(f"  - 发表日期: {metadata.get('publication_date', 'N/A')}")

        else:
            print(f"分析失败: {response.status_code}")
            print(response.json())

    except Exception as e:
        print(f"错误: {e}")


def get_paper_types_example():
    """获取支持的文献类型"""
    print("\n" + "="*60)
    print("示例5: 获取支持的文献类型")
    print("="*60)

    try:
        response = requests.get(f"{BASE_URL}/paper-types", timeout=10)
        result = response.json()

        for paper_type, info in result['supported_types'].items():
            print(f"\n{info['name']} ({paper_type}):")
            print(f"  描述: {info['description']}")
            print(f"  模块: {', '.join(info['modules'].keys())}")

    except Exception as e:
        print(f"错误: {e}")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("文献整理在线工具 - 使用示例")
    print("="*60)
    print("\n请确保服务已启动: python main.py")

    # 检查服务是否运行
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✓ 服务运行正常")
        else:
            print("✗ 服务未正常运行")
            return
    except:
        print("✗ 无法连接到服务，请先启动服务")
        print("  运行命令: python main.py")
        return

    # 运行示例
    analyze_text_example()
    analyze_case_report_example()
    analyze_basic_research_example()
    analyze_doi_example()
    get_paper_types_example()

    print("\n" + "="*60)
    print("所有示例完成！")
    print("="*60)


if __name__ == "__main__":
    main()
