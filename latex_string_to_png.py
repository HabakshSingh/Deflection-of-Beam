import pylab
#rcParams.update(matplotlib.rcParamsDefault)
def final_solution_image(formula):
    formula="Sorry! We couldn't render the solution!!\nBut we guarantee it's ready, enter 'x'"
    fig = pylab.figure()
    text = fig.text(0, 0, formula)
    dpi = 300
    fig.savefig(r'random_image.png', dpi=dpi)
    bbox = text.get_window_extent()
    width, height = bbox.size / float(dpi) + 0.005
    fig.set_size_inches((width, height))
    dy = (bbox.ymin/float(dpi))/height
    text.set_position((0, -dy))
    fig.savefig(r'random_image.png', dpi=dpi)

final_solution_image()