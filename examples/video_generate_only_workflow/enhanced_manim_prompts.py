# 初版待改进

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class ManimPromptTemplate:
    """Manim代码生成的提示词模板"""
    system_prompt: str
    user_prompt_template: str
    few_shot_examples: List[Dict[str, str]]
    validation_rules: List[str]

class EnhancedManimPromptSystem:
    """
    增强的Manim提示词系统
    """
    
    def __init__(self):
        self.templates = self._load_prompt_templates()
        self.few_shot_examples = self._load_few_shot_examples()
        self.validation_rules = self._load_validation_rules()
    
    def _load_prompt_templates(self):
        """加载不同类型的提示词模板"""
        # 基础系统提示词
        base_system_prompt = """
You are an expert Manim Community code generator. You ONLY respond with valid Manim code, nothing else.

# Critical Rules:
1. Always use 'Scene' as the base class (not VoiceoverScene unless specifically requested)
2. Always use 'construct' method as the main animation function
3. Always include proper imports: from manim import *
4. Use clear, descriptive variable names
5. Add helpful comments for complex animations
6. Follow Manim best practices for smooth animations

# Code Structure Template:
```python
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Your animation code here
        pass
```

IMPORTANT: Return ONLY the Python code, no explanations or markdown.
"""
        
        # 数学动画专用系统提示词
        math_system_prompt = """
You are a mathematical animation expert specializing in Manim Community.

# Mathematical Animation Rules:
1. Use LaTeX for all mathematical expressions: MathTex("\\frac{1}{2}")
2. Color-code different mathematical concepts consistently
3. Use proper mathematical notation and symbols
4. Include step-by-step visual proofs when applicable
5. Add geometric constructions that illustrate mathematical principles
6. Use coordinate systems when showing geometric relationships

# Standard Colors for Math:
- BLUE: Primary shapes and main concepts
- RED: Emphasis and important results  
- GREEN: Secondary elements and comparisons
- YELLOW: Highlights and final conclusions
- WHITE: Standard text and labels

# Animation Patterns for Math:
- Create(): For drawing geometric shapes
- Write(): For mathematical text and equations
- Transform(): For showing mathematical transformations
- Flash(): For emphasizing important results
- LaggedStart(): For sequential element animations

RETURN ONLY PYTHON CODE, NO EXPLANATIONS.
"""
        
        # 科普动画系统提示词
        educational_system_prompt = """
You are an educational animation specialist using Manim Community.

# Educational Animation Principles:
1. Start with simple concepts, build complexity gradually
2. Use clear visual hierarchies and consistent styling
3. Include titles and descriptive labels
4. Use smooth transitions between concepts
5. Provide visual feedback for key insights
6. Make animations self-explanatory through visual cues

# Educational Animation Structure:
1. Title/Introduction (2-3 seconds)
2. Main Content (progressive revelation)
3. Summary/Conclusion (emphasis)

# Recommended Timing:
- self.wait(1) for concept absorption
- run_time=2 for important transformations
- run_time=0.5 for quick transitions

RETURN ONLY PYTHON CODE, NO EXPLANATIONS.
"""
        
        return {
            "basic": ManimPromptTemplate(
                system_prompt=base_system_prompt,
                user_prompt_template="Generate Manim code for: {content}",
                few_shot_examples=[],
                validation_rules=["from manim import", "class", "Scene", "def construct"]
            ),
            "mathematical": ManimPromptTemplate(
                system_prompt=math_system_prompt,
                user_prompt_template="Create a mathematical animation for: {content}\n\nRequirements:\n{requirements}",
                few_shot_examples=[],
                validation_rules=["MathTex", "from manim import", "mathematical"]
            ),
            "educational": ManimPromptTemplate(
                system_prompt=educational_system_prompt,
                user_prompt_template="Create an educational animation explaining: {content}\n\nTarget audience: {audience}\nKey concepts: {concepts}",
                few_shot_examples=[],
                validation_rules=["Title", "self.wait", "progressive"]
            )
        }
    
    def _load_few_shot_examples(self):
        """加载少样本学习示例"""
        
        return {
            "mathematical": [
                {
                    "description": "Show the Pythagorean theorem with visual proof",
                    "code": '''from manim import *

class PythagoreanScene(Scene):
    def construct(self):
        # Title
        title = Tex("Pythagorean Theorem", font_size=48).to_edge(UP)
        self.play(Write(title))
        
        # Right triangle
        A = [-2, -1, 0]
        B = [2, -1, 0]  
        C = [-2, 2, 0]
        triangle = Polygon(A, B, C, color=BLUE, fill_opacity=0.3)
        self.play(Create(triangle))
        
        # Labels
        a_label = MathTex("a", color=RED).next_to(Line(A, C), LEFT)
        b_label = MathTex("b", color=GREEN).next_to(Line(A, B), DOWN)
        c_label = MathTex("c", color=YELLOW).next_to(Line(B, C), UR)
        self.play(Write(a_label), Write(b_label), Write(c_label))
        
        # Squares on each side
        square_a = Square(side_length=1.5, color=RED, fill_opacity=0.2).next_to(Line(A, C), LEFT, buff=0)
        square_b = Square(side_length=2, color=GREEN, fill_opacity=0.2).next_to(Line(A, B), DOWN, buff=0)
        
        self.play(Create(square_a), Create(square_b))
        
        # Equation
        equation = MathTex("a^2", "+", "b^2", "=", "c^2").to_edge(DOWN)
        equation.set_color_by_tex("a^2", RED)
        equation.set_color_by_tex("b^2", GREEN) 
        equation.set_color_by_tex("c^2", YELLOW)
        self.play(Write(equation))
        
        self.wait(2)'''
                },
                {
                    "description": "Visualize derivative as slope of tangent line",
                    "code": '''from manim import *

class DerivativeVisualization(Scene):
    def construct(self):
        # Set up axes
        axes = Axes(x_range=[-1, 4], y_range=[-1, 3])
        self.play(Create(axes))
        
        # Function curve
        func = axes.plot(lambda x: 0.5 * x**2, color=BLUE)
        func_label = MathTex("f(x) = \\\\frac{1}{2}x^2").to_corner(UL)
        self.play(Create(func), Write(func_label))
        
        # Point on curve
        x_val = 2
        point = Dot(axes.c2p(x_val, 0.5 * x_val**2), color=RED)
        self.play(Create(point))
        
        # Tangent line
        slope = x_val  # derivative of 0.5x^2 is x
        tangent = axes.plot(lambda x: slope * (x - x_val) + 0.5 * x_val**2, 
                           x_range=[x_val-1, x_val+1], color=RED)
        self.play(Create(tangent))
        
        # Slope label
        slope_label = MathTex(f"f'({x_val}) = {slope}").next_to(point, UR)
        self.play(Write(slope_label))
        
        self.wait(2)'''
                }
            ],
            "educational": [
                {
                    "description": "Explain machine learning concept step by step",
                    "code": '''from manim import *

class MLConceptScene(Scene):
    def construct(self):
        # Title with background
        title = Text("Machine Learning", font_size=48, color=BLUE)
        title_bg = SurroundingRectangle(title, color=BLUE, fill_opacity=0.1)
        self.play(DrawBorderThenFill(title_bg), Write(title))
        self.play(title.animate.scale(0.7).to_edge(UP))
        
        # Data points
        dots = VGroup(*[Dot(2*np.random.random(3)-1, color=BLUE) for _ in range(10)])
        self.play(LaggedStart(*[Create(dot) for dot in dots], lag_ratio=0.1))
        
        # Learning process
        line = Line(LEFT*2, RIGHT*2, color=RED)
        learning_text = Text("Learning Pattern...", font_size=24).to_edge(DOWN)
        self.play(Write(learning_text), Create(line))
        
        # Result
        result_text = Text("Pattern Found!", font_size=32, color=GREEN).to_edge(DOWN)
        self.play(Transform(learning_text, result_text))
        
        self.wait(2)'''
                }
            ]
        }
    
    def _load_validation_rules(self):
        """加载代码验证规则"""
        return {
            "required_imports": ["from manim import"],
            "required_structure": ["class", "Scene", "def construct"],
            "best_practices": ["self.play", "self.wait", "color="],
            "mathematical": ["MathTex", "LaTeX"],
            "educational": ["Text", "title", "explanation"]
        }
    
    def enhance_prompt_with_context(self, content, animation_type,context_info = None,few_shot = True):
        """
        增强提示词，添加上下文和少样本学习
        """
        
        template = self.templates.get(animation_type, self.templates["basic"])
        
        # 构建系统提示词
        system_prompt = template.system_prompt
        
        # 添加少样本示例
        if few_shot and animation_type in self.few_shot_examples:
            examples = self.few_shot_examples[animation_type]
            if examples:
                system_prompt += "\n\n# Example Code Patterns:\n"
                for i, example in enumerate(examples[:2]):  # 最多2个示例
                    system_prompt += f"\n## Example {i+1}: {example['description']}\n"
                    system_prompt += f"```python\n{example['code']}\n```\n"
        
        # 构建用户提示词
        if context_info is None:
            context_info = {}
        
        user_prompt = template.user_prompt_template.format(
            content=content,
            **context_info
        )
        
        # 添加特定要求
        requirements = self._generate_requirements(content, animation_type, context_info)
        if requirements:
            user_prompt += f"\n\nSpecific Requirements:\n{requirements}"
        
        return system_prompt, user_prompt
    
    def _generate_requirements(self, content, animation_type, context_info):
        """根据内容和类型生成具体要求"""
        
        requirements = []
        
        # 基础要求
        requirements.append("- Use clear, descriptive variable names")
        requirements.append("- Include appropriate wait times for viewing")
        requirements.append("- Use consistent color scheme")
        
        # 类型特定要求
        if animation_type == "mathematical":
            requirements.append("- Use LaTeX for all mathematical expressions")
            requirements.append("- Include proper mathematical notation")
            requirements.append("- Color-code different mathematical concepts")
            
            # 检测数学概念
            if any(keyword in content.lower() for keyword in ['theorem', 'proof', 'equation']):
                requirements.append("- Include step-by-step visual proof")
            if any(keyword in content.lower() for keyword in ['geometry', 'triangle', 'circle']):
                requirements.append("- Use geometric constructions")
        
        elif animation_type == "educational":
            requirements.append("- Start with a clear title")
            requirements.append("- Build concepts progressively") 
            requirements.append("- Include explanatory text")
            requirements.append("- End with summary or conclusion")
            
            # 根据上下文调整
            if context_info.get('audience') == 'beginner':
                requirements.append("- Use simple, clear animations")
                requirements.append("- Include more explanatory text")
        
        # 内容特定要求
        if any(keyword in content.lower() for keyword in ['data', 'graph', 'chart']):
            requirements.append("- Include proper axes and labels")
            requirements.append("- Use data visualization best practices")
        
        if any(keyword in content.lower() for keyword in ['process', 'step', 'algorithm']):
            requirements.append("- Show process step-by-step")
            requirements.append("- Use visual indicators for current step")
        
        return '\n'.join(requirements)
    
    def validate_generated_code(self, code, animation_type):
        """验证生成的代码质量"""
        
        issues = []
        suggestions = []
        score = 100
        
        # 基础验证
        if "from manim import" not in code:
            issues.append("Missing Manim imports")
            score -= 20
        
        if "class" not in code or "Scene" not in code:
            issues.append("Missing Scene class definition")
            score -= 25
        
        if "def construct" not in code:
            issues.append("Missing construct method")
            score -= 25
        
        if "self.play" not in code:
            issues.append("No animations found")
            score -= 15
        
        # 类型特定验证
        if animation_type == "mathematical":
            if "MathTex" not in code and "Tex" not in code:
                suggestions.append("Consider using MathTex for mathematical expressions")
                score -= 5
        
        elif animation_type == "educational":
            if "Text" not in code and "Tex" not in code:
                suggestions.append("Consider adding explanatory text")
                score -= 5
            
            if "title" not in code.lower():
                suggestions.append("Consider adding a title")
                score -= 3
        
        if "self.wait" not in code:
            suggestions.append("Consider adding wait times for better pacing")
        
        if "color=" not in code:
            suggestions.append("Consider using colors to enhance visual appeal")
        
        return {
            "score": max(0, score),
            "issues": issues,
            "suggestions": suggestions,
            "is_valid": len(issues) == 0
        }

    def create_enhanced_prompt(self, content, content_type= "educational", context_segments = None, main_theme = None, audio_duration = None):
        """
        创建增强的提示词，整合所有最佳实践
        """
        
        # 准备上下文信息
        context_info = {
            "audience": "general",
            "concepts": [],
            "requirements": ""
        }
        
        if main_theme:
            context_info["theme"] = main_theme
        
        if audio_duration:
            context_info["duration"] = f"approximately {audio_duration:.1f} seconds"
        
        if context_segments:
            # 从上下文段落中提取关键概念
            all_content = " ".join([seg.get('content', '') for seg in context_segments])
            context_info["full_context"] = all_content[:500]  # 限制长度
        
        # 这里是智能选择动画类型
        animation_type = self._detect_animation_type(content, content_type)
        
        # 生成增强提示词
        system_prompt, user_prompt = self.enhance_prompt_with_context(
            content=content,
            animation_type=animation_type,
            context_info=context_info,
            few_shot=True
        )
        return system_prompt, user_prompt
    
    def _detect_animation_type(self, content, content_type):
        """智能检测最佳动画类型"""
        
        content_lower = content.lower()
        math_keywords = ['equation', 'formula', 'theorem', 'proof', 'derivative', 'integral', 
                        'geometry', 'algebra', 'calculus', 'function', 'graph', 'plot']
        if any(keyword in content_lower for keyword in math_keywords):
            return "mathematical"
        
        edu_keywords = ['explain', 'understand', 'learn', 'concept', 'principle', 'theory',
                       'introduction', 'overview', 'basics', 'fundamental']
        if any(keyword in content_lower for keyword in edu_keywords):
            return "educational"
        
        if content_type in ['example', 'definition', 'explanation']:
            return "educational"
        elif content_type in ['mathematical', 'formula']:
            return "mathematical"
        
        return "educational" 


