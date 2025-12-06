"""
Scientists configuration for AI Expert Aggregator
AI 顶尖专家配置
"""

SCIENTISTS = {
    # ==================== OpenAI ====================
    "Alec Radford": {
        "org": "OpenAI",
        "role": "Distinguished Researcher",
        "role_cn": "研究员",
        "description": "GPT-1/2/3, CLIP, Whisper的核心作者",
        "aliases": ["Alec Radford"],
        "twitter": None,  # Very private, no public account
        "scholar_id": None,
    },
    "Jakub Pachocki": {
        "org": "OpenAI",
        "role": "Chief Scientist",
        "role_cn": "首席科学家",
        "description": "GPT-4项目总指挥，接替Ilya负责Scaling",
        "aliases": ["Jakub Pachocki", "Jakub W. Pachocki"],
        "twitter": None,
        "scholar_id": None,
    },
    "John Schulman": {
        "org": "Anthropic",  # Moved from OpenAI
        "role": "Co-founder (formerly OpenAI)",
        "role_cn": "联合创始人",
        "description": "ChatGPT之父，RLHF核心贡献者",
        "aliases": ["John Schulman"],
        "twitter": None,
        "scholar_id": None,
    },
    "Mark Chen": {
        "org": "OpenAI",
        "role": "VP of Research",
        "role_cn": "研发副总裁",
        "description": "负责o1/GPT-4o产品转化",
        "aliases": ["Mark Chen"],
        "twitter": None,
        "scholar_id": None,
    },
    
    # ==================== DeepMind ====================
    "Demis Hassabis": {
        "org": "DeepMind",
        "role": "CEO",
        "role_cn": "CEO",
        "description": "AlphaGo/AlphaFold之父，2024诺贝尔化学奖",
        "aliases": ["Demis Hassabis", "DeepMind CEO"],
        "twitter": "@demaboron",  # Rarely used
        "scholar_id": None,
    },
    "Jeff Dean": {
        "org": "Google",
        "role": "Chief Scientist",
        "role_cn": "首席科学家",
        "description": "谷歌AI守护神，MapReduce/TensorFlow作者",
        "aliases": ["Jeff Dean", "Jeffrey Dean"],
        "twitter": "@JeffDean",
        "scholar_id": None,
    },
    "Oriol Vinyals": {
        "org": "DeepMind",
        "role": "VP of Research",
        "role_cn": "研究副总裁",
        "description": "Gemini技术总负责人，Seq2Seq发明者",
        "aliases": ["Oriol Vinyals"],
        "twitter": "@OriolVinyalsML",
        "scholar_id": None,
    },
    
    # ==================== Anthropic ====================
    "Dario Amodei": {
        "org": "Anthropic",
        "role": "CEO",
        "role_cn": "CEO",
        "description": "Scaling Laws发现者",
        "aliases": ["Dario Amodei", "Anthropic CEO"],
        "twitter": "@DarioAmodei",
        "scholar_id": None,
    },
    "Jared Kaplan": {
        "org": "Anthropic",
        "role": "Co-founder",
        "role_cn": "联合创始人",
        "description": "Scaling Laws论文一作",
        "aliases": ["Jared Kaplan"],
        "twitter": None,
        "scholar_id": None,
    },
    "Chris Olah": {
        "org": "Anthropic",
        "role": "Co-founder",
        "role_cn": "联合创始人",
        "description": "机械可解释性大神",
        "aliases": ["Chris Olah", "Christopher Olah"],
        "twitter": "@ch402",
        "scholar_id": None,
    },
    
    # ==================== xAI ====================
    "Igor Babuschkin": {
        "org": "xAI",
        "role": "Core Tech Lead",
        "role_cn": "核心技术负责人",
        "description": "前DeepMind/OpenAI，Grok主要操盘手",
        "aliases": ["Igor Babuschkin"],
        "twitter": "@ibaboron",
        "scholar_id": None,
    },
    "Christian Szegedy": {
        "org": "xAI",
        "role": "Founding Member",
        "role_cn": "创始成员",
        "description": "Inception/BatchNorm/对抗样本提出者",
        "aliases": ["Christian Szegedy"],
        "twitter": None,
        "scholar_id": None,
    },
    "Zihang Dai": {
        "org": "xAI",
        "role": "Founding Member",
        "role_cn": "创始成员",
        "description": "XLNet一作，长上下文专家",
        "aliases": ["Zihang Dai", "戴子航"],
        "twitter": None,
        "scholar_id": None,
    },
    "Guodong Zhang": {
        "org": "xAI",
        "role": "Founding Member",
        "role_cn": "创始成员",
        "description": "前DeepMind，大模型训练稳定性专家",
        "aliases": ["Guodong Zhang", "张国栋"],
        "twitter": None,
        "scholar_id": None,
    },
    
    # ==================== Independent ====================
    "Ilya Sutskever": {
        "org": "SSI (Safe Superintelligence)",
        "role": "Founder",
        "role_cn": "创始人",
        "description": "前OpenAI首席科学家，深度学习先驱",
        "aliases": ["Ilya Sutskever"],
        "twitter": None,  # Very private
        "scholar_id": None,
    },
    "Bill Dally": {
        "org": "NVIDIA",
        "role": "Chief Scientist",
        "role_cn": "首席科学家",
        "description": "NVIDIA首席科学家，GPU计算架构大师",
        "aliases": ["Bill Dally", "William Dally", "William J. Dally"],
        "twitter": None,
        "scholar_id": None,
    },
    "Fei-Fei Li": {
        "org": "Stanford University",
        "role": "Professor",
        "role_cn": "教授",
        "description": "ImageNet创建者，AI4ALL创始人",
        "aliases": ["Fei-Fei Li", "Li Fei-Fei", "李飞飞"],
        "twitter": "@drfeifei",
        "scholar_id": None,
    },
}

def get_all_aliases():
    """Get all scientist name aliases for content matching"""
    aliases = []
    for name, info in SCIENTISTS.items():
        aliases.extend(info.get("aliases", [name]))
    return aliases

def get_scientist_by_alias(alias):
    """Find scientist info by any of their aliases"""
    for name, info in SCIENTISTS.items():
        if alias.lower() in [a.lower() for a in info.get("aliases", [name])]:
            return name, info
    return None, None
