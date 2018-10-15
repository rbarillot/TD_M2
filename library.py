from alinea.caribu.CaribuScene import CaribuScene
from alinea.caribu.sky_tools import GenSky, GetLight, Gensun, GetLightsSun
from openalea.plantgl.all import *
from numpy import arange
import matplotlib.pyplot as plt

def run_lsystem(scaling_Lmax=1, inclination_factor=1, lsys=None):
    lsys.scaling_Lmax = scaling_Lmax
    lsys.inclination_factor = inclination_factor
    lstring = lsys.animate()
    interpretedstring = lsys.interpret(lstring)
    scene = lsys.sceneInterpretation(interpretedstring)
    Viewer.display(scene)
    scene.save(r'plante.bgeom')
    return


def Light_model(lsys, lstring, hour=12):
    scene = lsys.sceneInterpretation(lstring)
    # Creates sun
    energy = 1
    DOY = 175
    latitude = 46.4333
    getsun = GetLightsSun.GetLightsSun(Gensun.Gensun()(energy, DOY, hour, latitude)).split(' ')
    sun = tuple((float(getsun[0]), tuple((float(getsun[1]), float(getsun[2]), float(getsun[3])))))
    sun_position = sun
    # print (sun_position)
    sun_shp = Shape(Translated(sun_position[1][0] * -50, sun_position[1][1] * -50, sun_position[1][2] * -50, Sphere(0.5)), Material(Color3(60, 60, 15)), id=0)
    scene.add(sun_shp)

    c_scene = CaribuScene(scene=scene, light=[sun])
    Viewer.display(scene)
    raw, aggregated = c_scene.run()

    # Visualisation
    viewmaponcan, _ = c_scene.plot(raw['default_band']['Eabs'], display=False)
    Viewer.display(viewmaponcan)

    # Graph
    graph = {'Tige': 0, 'Feuilles': 0}
    for vid, Eabs in aggregated['default_band']['Eabs'].items():
        if vid == 0:
            continue
        elif lstring[vid].name == 'F':
            graph['Feuilles'] += Eabs / sum(aggregated['default_band']['Eabs'].values())
        else:
            graph['Tige'] += Eabs / sum(aggregated['default_band']['Eabs'].values())

    # Graph
    fig, ax = plt.subplots()
    xindex = [1, 2]
    LABELS = graph.keys()
    ax.bar(xindex, graph.values(), align='center')
    plt.xticks(xindex, LABELS)
    ax.set_yticks(arange(0, 1.2, 0.2))
    ax.set_ylabel('Proportion interception PAR')


def Run_Asso(scene_asso, lsys_asso_str, distance=0):
    def Calcul_Caribu(scene):
        # ciel
        sky_string = GetLight.GetLight(GenSky.GenSky()(1, 'soc', 4, 5))  # (Energy, soc/uoc, azimuts, zenits)

        sky = []
        for string in sky_string.split('\n'):
            if len(string) != 0:
                string_split = string.split(' ')
                t = tuple((float(string_split[0]), tuple((float(string_split[1]), float(string_split[2]), float(string_split[3])))))
                sky.append(t)

        c_scene = CaribuScene(scene=scene, light=sky)
        Viewer.display(scene)
        raw, aggregated = c_scene.run()

        # Visualisation
        viewmaponcan, _ = c_scene.plot(raw['default_band']['Eabs'], display=False)
        Viewer.display(viewmaponcan)

        # Graph
        graph = {'luzerne': 0, 'fetuque': 0}
        eabs_total = sum(eabs * area for (eabs, area) in zip(aggregated['default_band']['Eabs'].values(), aggregated['default_band']['area'].values()))
        for vid, Eabs in aggregated['default_band']['Eabs'].items():
            if 'luzerne' in lsys_asso_str[vid]:
                graph['luzerne'] += Eabs * aggregated['default_band']['area'][vid] / eabs_total
            elif 'fetuque' in lsys_asso_str[vid]:
                graph['fetuque'] += Eabs * aggregated['default_band']['area'][vid] / eabs_total
            else:
                print ('vid', vid, lsys_asso_str[vid])

        fig, ax = plt.subplots()
        xindex = [1, 2]
        LABELS = graph.keys()
        ax.bar(xindex, graph.values(), align='center')
        plt.xticks(xindex, LABELS)
        ax.set_yticks(arange(0, 1.2, 0.2))
        ax.set_ylabel("Proportion interception PAR")

    scene_out = Scene()
    for i in range(len(scene_asso)):
        if 'fetuque' in lsys_asso_str[scene_asso[i].id]:
            scene_out += Shape(Translated(distance, 0, 0, scene_asso[i].geometry), scene_asso[i].appearance, id=scene_asso[i].id)
        else:
            scene_out += Shape(scene_asso[i].geometry, scene_asso[i].appearance, id=scene_asso[i].id)
    Calcul_Caribu(scene_out)
