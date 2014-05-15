def svg_css_link(svg_path):
    css_path = svg_path[ : svg_path.index('.')] + '.css'
    css_link = '<?xml-stylesheet type="text/css" href="{}"?>\n'.format(css_path)
    svg_file = open(svg_path, 'r+')
    lines = svg_file.readlines()
    lines.insert(1, css_link)
    svg_file.seek(0)
    svg_file.write(''.join(lines))
    svg_file.close()
