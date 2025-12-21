#!/usr/bin/env python3
"""
Gemini-Powered UI Design Assistant for Swim Stroke Analyzer
Analyzes the current UI and provides AI-powered design suggestions
"""

import os
import json
import base64
from datetime import datetime
from pathlib import Path

try:
    import google.generativeai as genai
except ImportError:
    print("❌ Error: google-generativeai not installed")
    print("Install it with: pip install google-generativeai")
    exit(1)


class UIDesignAssistant:
    def __init__(self, api_key=None):
        """Initialize the design assistant with Gemini API"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')

        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY environment variable "
                "or pass it to the constructor.\n\n"
                "Get your API key at: https://makersuite.google.com/app/apikey"
            )

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

        # Create output directory for design recommendations
        self.output_dir = Path('design_recommendations')
        self.output_dir.mkdir(exist_ok=True)

    def analyze_ui_structure(self):
        """Analyze the current UI code structure"""
        print("🔍 Analyzing UI structure...")

        ui_structure = {
            'components': [],
            'styles': {},
            'pages': []
        }

        # Read frontend components
        frontend_src = Path('frontend/src')
        if frontend_src.exists():
            # Read components
            components_dir = frontend_src / 'components'
            if components_dir.exists():
                for comp_file in components_dir.glob('*.js'):
                    with open(comp_file, 'r') as f:
                        ui_structure['components'].append({
                            'name': comp_file.stem,
                            'code': f.read()
                        })

            # Read main styles
            css_file = frontend_src / 'App.css'
            if css_file.exists():
                with open(css_file, 'r') as f:
                    ui_structure['styles']['main'] = f.read()

            # Read App.js
            app_file = frontend_src / 'App.js'
            if app_file.exists():
                with open(app_file, 'r') as f:
                    ui_structure['pages'].append({
                        'name': 'Main App',
                        'code': f.read()
                    })

        return ui_structure

    def generate_comprehensive_analysis(self, ui_structure):
        """Generate comprehensive UI analysis using Gemini"""
        print("🤖 Generating AI-powered design analysis...")

        prompt = f"""You are an expert UI/UX designer analyzing a swim stroke analyzer application.

**Application Context:**
- Purpose: AI-powered freestyle swimming technique analysis
- Target Users: Swimmers, coaches, fitness enthusiasts
- Key Features: Video upload, pose detection analysis, technique feedback

**Current UI Structure:**

COMPONENTS:
{json.dumps([{'name': c['name'], 'code_preview': c['code'][:500]} for c in ui_structure['components']], indent=2)}

MAIN STYLES (CSS):
{ui_structure['styles'].get('main', 'No styles found')[:1500]}

**Your Task:**
Provide a comprehensive UI/UX analysis with the following sections:

1. **OVERALL IMPRESSION** (2-3 sentences)
   - What works well
   - Main areas for improvement

2. **COLOR SCHEME ANALYSIS**
   - Current color palette assessment
   - Suggested improvements or alternatives
   - Color psychology for sports/fitness apps

3. **LAYOUT & STRUCTURE**
   - Current layout strengths/weaknesses
   - Suggested layout improvements
   - Responsive design considerations

4. **USER EXPERIENCE**
   - User flow analysis
   - Pain points
   - Suggested UX improvements

5. **MODERN UI TRENDS**
   - How to incorporate glassmorphism, neumorphism, or other modern trends
   - Animation suggestions
   - Micro-interactions to add

6. **SPECIFIC COMPONENT IMPROVEMENTS**
   For each major component (Upload, Processing, Results):
   - What works
   - What to improve
   - Specific design suggestions

7. **ACCESSIBILITY**
   - Current accessibility issues
   - WCAG compliance suggestions
   - Inclusive design recommendations

8. **ACTIONABLE NEXT STEPS**
   Prioritized list of top 10 improvements to implement, ordered by impact.

Please be specific and actionable. Include color codes, spacing values, and concrete examples.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ Error generating analysis: {e}")
            return None

    def generate_color_palette_suggestions(self):
        """Generate modern color palette suggestions specific to swimming"""
        print("🎨 Generating color palette suggestions...")

        prompt = """As a UI designer, create 3 modern color palette suggestions for a swim stroke analyzer app.

For each palette, provide:
1. **Palette Name** (creative, relevant to swimming/water)
2. **Primary Colors** (with hex codes)
3. **Secondary Colors** (with hex codes)
4. **Accent Colors** (with hex codes)
5. **Background/Neutral Colors** (with hex codes)
6. **CSS Variables Code** (ready to use)
7. **Use Case Description** (when to use each color)
8. **Mood/Psychology** (what feeling this palette evokes)

Make palettes modern, accessible (WCAG AA compliant), and suitable for a sports/fitness application.
Consider water, energy, clarity, and performance as themes.

Format each palette clearly with actual hex codes I can copy-paste into CSS.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ Error generating color palettes: {e}")
            return None

    def generate_component_redesigns(self, component_name, component_code):
        """Generate specific redesign suggestions for a component"""
        print(f"🎯 Generating redesign for {component_name}...")

        prompt = f"""As a React/UI expert, redesign this component: {component_name}

**Current Code:**
```javascript
{component_code}
```

**Provide:**

1. **Current Issues** (list 3-5 problems with current design)

2. **Redesign Concept** (describe the improved version)

3. **Improved React Component Code** (complete, production-ready)
   - Modern React best practices
   - Better state management
   - Improved accessibility
   - Enhanced visual design
   - Smooth animations/transitions

4. **Enhanced CSS** (modern, responsive styles)
   - Use CSS Grid/Flexbox effectively
   - Add smooth transitions
   - Responsive breakpoints
   - Modern effects (gradients, shadows, etc.)

5. **Why This is Better** (explain the improvements)

Make it modern, beautiful, and user-friendly. Focus on swim/sports aesthetic.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ Error generating component redesign: {e}")
            return None

    def generate_animation_suggestions(self):
        """Generate animation and micro-interaction suggestions"""
        print("✨ Generating animation suggestions...")

        prompt = """As a UI animation expert, suggest animations and micro-interactions for a swim stroke analyzer app.

Provide:

1. **Page Transitions**
   - Upload → Processing → Results flow
   - Suggested CSS/JS animations with code

2. **Loading States**
   - Video upload progress
   - Analysis processing
   - Creative swimming-themed loaders
   - Code examples

3. **Micro-Interactions**
   - Button hover effects
   - File drop animations
   - Success/error feedback
   - Data visualization animations
   - Code examples for each

4. **Performance Considerations**
   - How to keep animations smooth
   - GPU acceleration tips
   - When to use CSS vs JS animations

5. **Ready-to-Use CSS Code**
   - Complete keyframe animations
   - Transition utilities
   - Animation timing functions

Make animations feel fluid like water, energetic like swimming, and professional.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ Error generating animation suggestions: {e}")
            return None

    def generate_layout_alternatives(self):
        """Generate alternative layout suggestions"""
        print("📐 Generating layout alternatives...")

        prompt = """As a UI designer, suggest 3 alternative layout approaches for a swim stroke analyzer app.

Current flow: Upload → Processing → Results (linear, single page app)

For each alternative layout, provide:

1. **Layout Name & Concept**

2. **Visual Structure Description**
   - How elements are arranged
   - Use of whitespace
   - Grid/Flexbox approach

3. **Pros & Cons**
   - Benefits of this layout
   - Potential drawbacks

4. **When to Use**
   - Best use cases

5. **CSS Grid/Flexbox Code**
   - Actual implementation code
   - Responsive breakpoints

6. **Screenshot Description**
   - Detailed description of what this would look like

Consider:
- Dashboard-style layouts
- Split-screen comparisons
- Card-based layouts
- Timeline/step-based layouts
- Data-heavy analytical layouts
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ Error generating layout alternatives: {e}")
            return None

    def save_recommendations(self, analysis_data):
        """Save all design recommendations to files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save main analysis
        analysis_file = self.output_dir / f'ui_analysis_{timestamp}.md'
        with open(analysis_file, 'w') as f:
            f.write(f"# UI Design Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(analysis_data.get('comprehensive_analysis', ''))

        print(f"✅ Saved comprehensive analysis: {analysis_file}")

        # Save color palettes
        if 'color_palettes' in analysis_data:
            palette_file = self.output_dir / f'color_palettes_{timestamp}.md'
            with open(palette_file, 'w') as f:
                f.write(f"# Color Palette Suggestions\n\n")
                f.write(analysis_data['color_palettes'])
            print(f"✅ Saved color palettes: {palette_file}")

        # Save component redesigns
        if 'component_redesigns' in analysis_data:
            for comp_name, redesign in analysis_data['component_redesigns'].items():
                comp_file = self.output_dir / f'{comp_name}_redesign_{timestamp}.md'
                with open(comp_file, 'w') as f:
                    f.write(f"# {comp_name} Component Redesign\n\n")
                    f.write(redesign)
                print(f"✅ Saved {comp_name} redesign: {comp_file}")

        # Save animations
        if 'animations' in analysis_data:
            anim_file = self.output_dir / f'animations_{timestamp}.md'
            with open(anim_file, 'w') as f:
                f.write(f"# Animation Suggestions\n\n")
                f.write(analysis_data['animations'])
            print(f"✅ Saved animation suggestions: {anim_file}")

        # Save layouts
        if 'layouts' in analysis_data:
            layout_file = self.output_dir / f'layout_alternatives_{timestamp}.md'
            with open(layout_file, 'w') as f:
                f.write(f"# Layout Alternatives\n\n")
                f.write(analysis_data['layouts'])
            print(f"✅ Saved layout alternatives: {layout_file}")

        # Create summary file
        summary_file = self.output_dir / f'SUMMARY_{timestamp}.md'
        with open(summary_file, 'w') as f:
            f.write(f"# Design Assistant Summary\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Generated Files\n\n")
            f.write(f"- Comprehensive Analysis: `ui_analysis_{timestamp}.md`\n")
            f.write(f"- Color Palettes: `color_palettes_{timestamp}.md`\n")
            f.write(f"- Animation Suggestions: `animations_{timestamp}.md`\n")
            f.write(f"- Layout Alternatives: `layout_alternatives_{timestamp}.md`\n")
            f.write(f"- Component Redesigns: `*_redesign_{timestamp}.md`\n\n")
            f.write(f"## Quick Start\n\n")
            f.write(f"1. Read the comprehensive analysis first\n")
            f.write(f"2. Review color palette options\n")
            f.write(f"3. Choose component redesigns to implement\n")
            f.write(f"4. Add suggested animations\n")
            f.write(f"5. Consider layout alternatives if needed\n")

        print(f"\n✅ All recommendations saved to: {self.output_dir}/")
        print(f"📋 Start with: {summary_file}")

    def run_full_analysis(self):
        """Run complete UI design analysis"""
        print("\n" + "="*60)
        print("🏊‍♂️ Gemini-Powered UI Design Assistant")
        print("="*60 + "\n")

        analysis_data = {}

        # Step 1: Analyze UI structure
        ui_structure = self.analyze_ui_structure()

        # Step 2: Generate comprehensive analysis
        analysis_data['comprehensive_analysis'] = self.generate_comprehensive_analysis(ui_structure)

        # Step 3: Generate color palettes
        analysis_data['color_palettes'] = self.generate_color_palette_suggestions()

        # Step 4: Generate component redesigns
        analysis_data['component_redesigns'] = {}
        for component in ui_structure['components']:
            redesign = self.generate_component_redesigns(
                component['name'],
                component['code']
            )
            if redesign:
                analysis_data['component_redesigns'][component['name']] = redesign

        # Step 5: Generate animation suggestions
        analysis_data['animations'] = self.generate_animation_suggestions()

        # Step 6: Generate layout alternatives
        analysis_data['layouts'] = self.generate_layout_alternatives()

        # Step 7: Save everything
        self.save_recommendations(analysis_data)

        print("\n" + "="*60)
        print("✅ Design analysis complete!")
        print("="*60 + "\n")


def main():
    """Main entry point"""
    print("\n🏊‍♂️ Swim Stroke Analyzer - UI Design Assistant\n")

    # Check for API key
    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        print("❌ GEMINI_API_KEY environment variable not set")
        print("\n📝 To get started:")
        print("1. Get your API key: https://makersuite.google.com/app/apikey")
        print("2. Set environment variable:")
        print("   export GEMINI_API_KEY='your-api-key-here'")
        print("3. Run this script again")
        return

    try:
        assistant = UIDesignAssistant(api_key)
        assistant.run_full_analysis()

        print("\n💡 Next Steps:")
        print("1. Review the generated recommendations in design_recommendations/")
        print("2. Start with the SUMMARY file")
        print("3. Implement the top priority suggestions")
        print("4. Test and iterate!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
