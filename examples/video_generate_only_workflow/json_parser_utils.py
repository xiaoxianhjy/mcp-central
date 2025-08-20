# JSON解析工具模块

import json
import re
from typing import Dict, List, Any, Optional

def extract_json_robust(response):
    """
    加强json提取
    """
    
    # 1：直接解析整个响应
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError:
        pass
    
    # 2：提取```json```包围的内容
    json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1).strip())
        except json.JSONDecodeError:
            pass
    
    # 3：提取```包围的内容
    code_match = re.search(r'```\s*(.*?)\s*```', response, re.DOTALL)
    if code_match:
        try:
            return json.loads(code_match.group(1).strip())
        except json.JSONDecodeError:
            pass
    
    # 4：寻找大括号包围的JSON对象
    brace_matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
    for match in brace_matches:
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue
    
    # 5：寻找方括号包围的JSON数组
    bracket_matches = re.findall(r'\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]', response, re.DOTALL)
    for match in bracket_matches:
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue
    
    print(f"JSON解析失败，响应内容: {response[:200]}...")
    return None

def extract_json_with_fallback(response, fallback_value = None):
    """
    带有回退值的JSON提取
    """
    result = extract_json_robust(response)
    if result is not None:
        return result
    
    print(f"JSON解析失败，使用回退值: {fallback_value}")
    return fallback_value

def safe_json_parse(response, expected_keys = None):
    """
    安全的JSON解析，验证必需的键
    """
    result = extract_json_robust(response)
    
    if result is None:
        print("JSON解析失败，返回空字典")
        return {}
    
    if expected_keys:
        missing_keys = [key for key in expected_keys if key not in result]
        if missing_keys:
            print(f"JSON缺少必需的键: {missing_keys}")
            # 这里我给缺失的键提供默认值
            for key in missing_keys:
                result[key] = None
    
    return result

def clean_json_response(response):
    """
    清理响应文本，移除可能干扰JSON解析的内容
    """
    # 这里我移除了常见的前缀文本
    prefixes_to_remove = [
        "这是分析结果：",
        "分析结果如下：",
        "以下是JSON格式的结果：",
        "Here is the result:",
        "Here's the analysis:",
    ]
    
    cleaned = response.strip()
    for prefix in prefixes_to_remove:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
    
    # 移除常见的后缀文本
    suffixes_to_remove = [
        "以上就是分析结果。",
        "希望这个结果对您有帮助。",
        "如有疑问请随时询问。",
    ]
    
    for suffix in suffixes_to_remove:
        if cleaned.endswith(suffix):
            cleaned = cleaned[:-len(suffix)].strip()
    
    return cleaned

def validate_segments_json(data):
    """
    验证段落JSON数据的完整性
    """
    if not isinstance(data, dict):
        return False
    
    required_keys = ['segments']
    if not all(key in data for key in required_keys):
        return False
    
    segments = data.get('segments', [])
    if not isinstance(segments, list):
        return False
    
    for i, segment in enumerate(segments):
        if not isinstance(segment, dict):
            print(f"段落 {i} 不是字典格式")
            return False
        
        segment_required_keys = ['type', 'content']
        if not all(key in segment for key in segment_required_keys):
            print(f"段落 {i} 缺少必需的键: {segment_required_keys}")
            return False
    
    return True

def validate_analysis_json(data):
    """
    验证分析JSON数据的完整性
    """
    if not isinstance(data, dict):
        return False
    
    required_keys = ['topic', 'style', 'key_concepts']
    if not all(key in data for key in required_keys):
        missing = [key for key in required_keys if key not in data]
        print(f"分析数据缺少必需的键: {missing}")
        return False
    
    return True
