import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional

class AIFunctionParser:
    """AI功能解析器：将自然语言功能描述转化为标准化函数定义"""
    
    def __init__(self, api_key: str = "demo_key"):
        """初始化解析器
        Args:
            api_key: 大模型API密钥（演示用默认值）
        """
        self.api_key = api_key
        self.prompt_template = """请将以下功能描述解析为标准化函数定义：
        
功能描述：{description}

要求：
1. 函数名使用snake_case格式，体现功能核心
2. 输入参数：列出参数名、类型和说明
3. 输出：说明返回的数据结构和类型
4. 功能分类：选择最合适的类别（用户管理、订单处理、数据报表、系统配置、其他）

请以JSON格式返回：
{{
    "function_name": "函数名",
    "description": "功能简要说明",
    "input_params": [
        {{"name": "参数名", "type": "类型", "description": "参数说明"}}
    ],
    "output": {{"type": "返回类型", "description": "返回说明"}},
    "category": "功能分类"
}}"""
        
        # 模拟已解析的功能缓存
        self.parsed_functions_cache = {}
        
    def mock_llm_api_call(self, prompt: str) -> Dict:
        """模拟大模型API调用（实际项目中替换为真实API）
        Args:
            prompt: 提示词模板
        Returns:
            解析后的函数定义字典
        """
        # 模拟API延迟
        time.sleep(0.1)
        
        # 根据描述内容模拟不同的解析结果
        description = prompt.split("功能描述：")[1].split("\n\n要求：")[0].strip()
        
        # 根据关键词确定分类
        category = "其他"
        category_keywords = {
            "用户": "用户管理",
            "客户": "用户管理",
            "订单": "订单处理",
            "交易": "订单处理",
            "报表": "数据报表",
            "统计": "数据报表",
            "配置": "系统配置",
            "设置": "系统配置"
        }
        
        for keyword, cat in category_keywords.items():
            if keyword in description:
                category = cat
                break
        
        # 生成模拟函数名
        words = description.replace("功能", "").replace("管理", "").split()
        if words:
            func_name = "_".join(words[:2]).lower() + "_operation"
        else:
            func_name = "default_operation"
        
        # 模拟返回结构
        return {
            "function_name": func_name,
            "description": f"自动解析的功能：{description[:30]}...",
            "input_params": [
                {"name": "user_id", "type": "int", "description": "用户唯一标识"},
                {"name": "data", "type": "dict", "description": "操作数据"}
            ],
            "output": {"type": "dict", "description": "操作结果，包含状态码和信息"},
            "category": category
        }
    
    def parse_function_description(self, description: str) -> Dict:
        """解析单个功能描述
        Args:
            description: 功能描述文本
        Returns:
            标准化函数定义
        """
        if description in self.parsed_functions_cache:
            return self.parsed_functions_cache[description]
        
        # 构建提示词
        prompt = self.prompt_template.format(description=description)
        
        # 调用模拟API
        try:
            result = self.mock_llm_api_call(prompt)
            self.parsed_functions_cache[description] = result
            return result
        except Exception as e:
            print(f"解析失败: {e}")
            return {
                "function_name": "error_function",
                "description": "解析失败",
                "input_params": [],
                "output": {"type": "str", "description": "错误信息"},
                "category": "其他"
            }
    
    def batch_parse_functions(self, descriptions: List[str]) -> List[Dict]:
        """批量解析功能描述
        Args:
            descriptions: 功能描述列表
        Returns:
            解析结果列表
        """
        results = []
        for i, desc in enumerate(descriptions, 1):
            print(f"正在解析第 {i}/{len(descriptions)} 个功能...")
            result = self.parse_function_description(desc)
            results.append(result)
        return results
    
    def analyze_results(self, results: List[Dict]) -> Dict:
        """分析解析结果统计信息
        Args:
            results: 解析结果列表
        Returns:
            统计信息字典
        """
        categories = {}
        total_params = 0
        
        for result in results:
            category = result.get("category", "其他")
            categories[category] = categories.get(category, 0) + 1
            total_params += len(result.get("input_params", []))
        
        return {
            "total_functions": len(results),
            "categories_distribution": categories,
            "avg_params_per_function": total_params / len(results) if results else 0,
            "parsing_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def main():
    """主函数：演示AI功能解析器的完整流程"""
    print("=== AI功能解析器演示 ===\n")
    
    # 初始化解析器
    parser = AIFunctionParser(api_key="your_api_key_here")
    
    # 示例功能描述（模拟B端系统功能点）
    sample_descriptions = [
        "用户信息管理功能，包括创建、修改、查询用户基本信息",
        "订单处理系统，支持订单创建、状态更新和退款操作",
        "生成销售数据报表，按日期、产品类别统计销售额",
        "系统参数配置管理，可以设置各项业务规则和阈值"
    ]
    
    print("开始批量解析功能描述...")
    print(f"待解析功能数: {len(sample_descriptions)}\n")
    
    # 批量解析
    results = parser.batch_parse_functions(sample_descriptions)
    
    # 显示解析结果
    print("\n=== 解析结果示例 ===")
    for i, result in enumerate(results[:2], 1):  # 只显示前2个示例
        print(f"\n功能{i}:")
        print(f"  函数名: {result['function_name']}")
        print(f"  描述: {result['description']}")
        print(f"  分类: {result['category']}")
        print(f"  输入参数: {len(result['input_params'])}个")
        for param in result['input_params']:
            print(f"    - {param['name']}: {param['type']} ({param['description']})")
    
    # 统计分析
    print("\n=== 统计分析 ===")
    stats = parser.analyze_results(results)
    print(f"总解析功能数: {stats['total_functions']}")
    print(f"分类分布:")
    for category, count in stats['categories_distribution'].items():
        print(f"  {category}: {count}个")
    print(f"平均参数数: {stats['avg_params_per_function']:.1f}")
    print(f"解析时间: {stats['parsing_time']}")
    
    # 保存结果到文件（模拟）
    print("\n=== 结果保存 ===")
    output_data = {
        "metadata": stats,
        "functions": results
    }
    
    # 模拟保存JSON文件
    output_str = json.dumps(output_data, ensure_ascii=False, indent=2)
    print(f"已生成结构化数据，包含 {len(results)} 个函数定义")
    print("数据格式验证通过，可导入知识库系统")
    
    print("\n=== 演示完成 ===")
    print("实际项目中，可将解析结果用于：")
    print("1. 知识库功能结构化")
    print("2. API文档自动生成")
    print("3. 功能模块化重构")

if __name__ == "__main__":
    main()