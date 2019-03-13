import numpy as np
import matplotlib.pyplot as plt
from tempfile import gettempdir
import os
from matplotlib import font_manager, rc

font_name = font_manager.FontProperties(fname='/usr/share/fonts/truetype/nanum/NanumGothic.ttf').get_name()

rc('font',family=font_name)
 
N = 50
area = np.pi * (15 * np.random.rand(N))**2
plt.scatter(np.random.rand(N), 
            np.random.rand(N), 
            s=area, 
            c=np.random.rand(N), 
            alpha=0.5)
plt.title("제발")
plt.ylabel("와이축")
plt.xlabel("엑스축")
tt = os.path.join(gettempdir(), 'test.png')
plt.savefig(tt)
