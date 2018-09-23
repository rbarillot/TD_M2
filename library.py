from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from openalea.plantgl.all import Viewer

#affichage regles interpretation Lsystem

def affichage_interpretation():
    print ('Regles interpretation \n\n','interpretation: \n\
    S(length, inclination, azimut, espece, radius): \n\
      produce ;(7) EulerAngles(azimut,inclination,0) F(length, 2) \n\
    \n\
    U(length, inclination, azimut, espece):\n\
      lf, la, pe, br, crois = 21./21., 6.5/21., 17./21., 3.6/21., 10./21. #leaf Trudeau\n\
      alpha = 3.14/8 #degre \n\
      leaf = mesh_leaflet(lf, la, alpha, 10)\n\
      inclination *= inclination_factor\n\
      produce ;(7) EulerAngles(azimut+90, 90, 0) +(inclination) @g(leaf, length*scaling_Lmax) EulerAngles(azimut, 90, 0) +(inclination) @g(leaf, length*scaling_Lmax) EulerAngles(azimut+180, 90, 0) +(inclination) @g(leaf, length*scaling_Lmax)\n\
    \n\
    T(length, inclination, azimut, espece):\n\
      produce ;(7) EulerAngles(azimut,inclination,0) F(length,0.2)')
    return


def run_lsystem(scaling_Lmax=1, inclination_factor=1, lsys=None):
    lsys.scaling_Lmax = scaling_Lmax
    lsys.inclination_factor = inclination_factor
    lstring = lsys.animate()
    interpretedstring = lsys.interpret(lstring)
    scene = lsys.sceneInterpretation(interpretedstring)
    Viewer.display(scene)
    scene.save(r'plante.bgeom')
    return lstring


# from alinea.caribu.CaribuScene import CaribuScene
# from alinea.caribu.sky_tools import GenSky, GetLight, Gensun, GetLightsSun
# from openalea.plantgl.all import *
#
# interpretedstring = lsys.interpret(lstring)
# scene = lsys.sceneInterpretation(lstring)

# def Light_model(hour=12):
#     # Creates sun
#     energy = 1
#     DOY = 175
#     latitude = 46.4333
#     getsun = GetLightsSun.GetLightsSun(Gensun.Gensun()(energy, DOY, hour, latitude)).split(' ')
#     sun = tuple((float(getsun[0]), tuple((float(getsun[1]), float(getsun[2]), float(getsun[3])))))
#     sun_position = sun
#     print (sun_position)
#     sun_shp = Shape(Translated(sun_position[1][0] * -50, sun_position[1][1] * -50, sun_position[1][2] * -50, Sphere(0.5)), Material(Color3(60, 60, 15)), id=0)
#     scene.add(sun_shp)
#
#
#     c_scene = CaribuScene(scene=scene, light=[sun])
#     Viewer.display(scene)
#     raw, aggregated = c_scene.run()
#
#     # Visualisation
#     viewmaponcan, _ = c_scene.plot(raw['default_band']['Eabs'], display=False)
#     Viewer.display(viewmaponcan)
#
#     # Graph
#     import matplotlib
#     import matplotlib.pyplot as plt
#     %matplotlib inline
#
#     graph = {'Tige':0, 'Feuilles':0}
#     for vid, Eabs in aggregated['default_band']['Eabs'].items():
#         if vid == 0: continue
#         elif lstring[vid].name == 'F':
#             graph['Feuilles'] += Eabs / sum(aggregated['default_band']['Eabs'].values())
#         else:
#             graph['Tige'] += Eabs / sum(aggregated['default_band']['Eabs'].values())
#
#     xindex = [1, 2]
#     LABELS = graph.keys()
#     plt.bar(xindex, graph.values(), align='center')
#     plt.xticks(xindex, LABELS)