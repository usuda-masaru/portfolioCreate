from django import template
import markdown
from datetime import datetime
from dateutil.relativedelta import relativedelta

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply the value by the argument"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def split(value, arg):
    """Split the value by the argument"""
    try:
        return value.split(arg)
    except (ValueError, TypeError, AttributeError):
        return []

@register.filter
def category_icon(category_name):
    """Get icon class for skill category"""
    icon_mapping = {
        'frontend': 'paint-brush',
        'backend': 'server',
        'database': 'database',
        'infrastructure': 'cloud',
        'framework': 'layer-group',
        'cloud': 'cloud',
        'tools': 'tools',
        'other': 'code'
    }
    return icon_mapping.get(category_name, 'code')

@register.filter
def language_color(language):
    """Get color for programming language"""
    color_mapping = {
        'Python': '#3776ab',
        'JavaScript': '#f7df1e',
        'TypeScript': '#3178c6',
        'Java': '#ed8b00',
        'C': '#a8b9cc',
        'C++': '#00599c',
        'C#': '#239120',
        'PHP': '#777bb4',
        'Ruby': '#cc342d',
        'Go': '#00add8',
        'Rust': '#000000',
        'Swift': '#fa7343',
        'Kotlin': '#7f52ff',
        'Dart': '#0175c2',
        'HTML': '#e34f26',
        'CSS': '#1572b6',
        'Sass': '#cc6699',
        'Vue': '#4fc08d',
        'React': '#61dafb',
        'Angular': '#dd0031',
        'Node.js': '#339933',
        'Shell': '#89e051',
        'PowerShell': '#012456',
        'R': '#276dc3',
        'MATLAB': '#0076a8',
        'Jupyter Notebook': '#da5b0b',
        'Dockerfile': '#384d54',
        'YAML': '#cb171e',
        'JSON': '#000000',
        'XML': '#0060ac',
        'Markdown': '#083fa1',
    }
    return color_mapping.get(language, '#6b7280')

@register.filter
def trim(value):
    """Remove leading and trailing whitespace"""
    if value is None:
        return ''
    return str(value).strip()

@register.filter
def markdown_to_html(value):
    """Convert markdown text to HTML"""
    if value is None:
        return ''
    # Configure markdown with extensions for better formatting
    md = markdown.Markdown(extensions=[
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists'
    ])
    return md.convert(str(value))

@register.filter
def duration_format(experience):
    """Calculate and format the duration between start_date and end_date"""
    if not experience or not hasattr(experience, 'start_date'):
        return ''
    
    start_date = experience.start_date
    if not start_date:
        return ''
    
    # 終了日を決定（is_currentがTrueまたはend_dateがNoneの場合は現在日付を使用）
    if experience.is_current or not experience.end_date:
        end_date = datetime.now().date()
    else:
        end_date = experience.end_date
    
    # relativedeltaを使用して正確な年月を計算
    delta = relativedelta(end_date, start_date)
    
    # 月数を計算（15日以上は1ヶ月として繰り上げ）
    total_months = delta.years * 12 + delta.months
    if delta.days >= 15:
        total_months += 1
    
    # 月数が0の場合は1ヶ月とする
    if total_months == 0:
        return "1ヶ月"
    
    # 年と月に分けて表示
    years = total_months // 12
    months = total_months % 12
    
    parts = []
    if years > 0:
        parts.append(f"{years}年")
    if months > 0:
        parts.append(f"{months}ヶ月")
    
    return "".join(parts)