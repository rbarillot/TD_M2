from alinea.caribu.CaribuScene import CaribuScene
from alinea.caribu.sky_tools import GenSky, GetLight, Gensun, GetLightsSun
from openalea.plantgl.all import *
from pgljupyter import SceneWidget
from numpy import arange
import matplotlib.pyplot as plt
from openalea.lpy import Lsystem


def reformat_scene(geometry):
    nbpolygons = len(geometry.indexList)
    sc = Scene()
    for i in range(nbpolygons):
        pts = [geometry.pointAt(i, j) for j in range(3)]
        c = geometry.colorList[i]
        sc.add(Shape(TriangleSet(pts, [list(range(3))]), Material((c.red, c.green, c.blue), 1, transparency=c.clampedAlpha())))
    return sc


def Light_model(lsys, hour=12):
    lstring = lsys.get_lstring()
    scene = lsys.scene['scene']
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
    # SceneWidget(scene)
    raw, aggregated = c_scene.run()

    # Visualisation
    viewmaponcan, _ = c_scene.plot(raw['default_band']['Eabs'], display=False)

    #  Fred's hack to display the scene with colors using pgl-jupyter widgets
    colored_scene = Scene()
    for shp in viewmaponcan:
        colored_scene.add(reformat_scene(shp.geometry))

    #  Graph
    graph = {'Tige': 0, 'Feuilles': 0}
    for vid, Eabs in aggregated['default_band']['Eabs'].items():
        if vid == 0:
            continue
        elif lstring[vid].name == 'F':
            graph['Feuilles'] += Eabs / sum(aggregated['default_band']['Eabs'].values())
        else:
            graph['Tige'] += Eabs / sum(aggregated['default_band']['Eabs'].values())

    fig, ax = plt.subplots()

    LIE = sum(aggregated['default_band']['Eabs'][k]*aggregated['default_band']['area'][k]*1E-4 for k in aggregated['default_band']['Eabs']) / (sum(aggregated['default_band']['area'].values())*1E-4)
    print("Efficience interception lumière = {}".format(LIE))

    xindex = [1, 2]
    LABELS = graph.keys()
    ax.bar(xindex, graph.values(), align='center')
    plt.xticks(xindex, LABELS)
    ax.set_yticks(arange(0, 1.2, 0.2))
    ax.set_ylabel('Proportion interception PAR')
    return SceneWidget(colored_scene, size_world=75)


def Run_Asso(distance=0, scaling_Lmax=1, inclination_factor=1):
    def Calcul_Caribu(scene):
        # ciel
        sky_string = GetLight.GetLight(GenSky.GenSky()(1, 'soc', 4, 5))  # (Energy, soc/uoc, azimuts, zenits)

        sky = []
        for string in sky_string.split('\n'):
            if len(string) != 0:
                string_split = string.split(' ')
                t = tuple((float(string_split[0]), tuple((float(string_split[1]), float(string_split[2]), float(string_split[3])))))
                sky.append(t)

        c_scene = CaribuScene(scene=scene, light=sky, pattern=(BoundingBox(scene).getXMin(), BoundingBox(scene).getYMin(), BoundingBox(scene).getXMax(), BoundingBox(scene).getYMax()))
        raw, aggregated = c_scene.run(direct=True, infinite=True)

        # Visualisation
        viewmaponcan, _ = c_scene.plot(raw['default_band']['Eabs'], display=False)

        #  Fred's hack to display the scene with colors using pgl-jupyter widgets
        colored_scene = Scene()
        for shp in viewmaponcan:
            colored_scene.add(reformat_scene(shp.geometry))

        # Graph
        graph = {'luzerne': 0, 'fetuque': 0}
        eabs_total = sum(eabs * area for (eabs, area) in zip(aggregated['default_band']['Eabs'].values(), aggregated['default_band']['area'].values()))
        for vid, Eabs in aggregated['default_band']['Eabs'].items():
            if vid >= 1000:
                graph['luzerne'] += Eabs * aggregated['default_band']['area'][vid] / eabs_total
            else:
                graph['fetuque'] += Eabs * aggregated['default_band']['area'][vid] / eabs_total

        fig, ax = plt.subplots()
        xindex = [1, 2]
        LABELS = graph.keys()
        ax.bar(xindex, graph.values(), align='center')
        plt.xticks(xindex, LABELS)
        ax.set_yticks(arange(0, 1.2, 0.2))
        ax.set_ylabel("Proportion interception PAR")

        return colored_scene

    # Makes Lsystem for association
    lsys_luz = Lsystem('TD_lsystem_Luzerne.lpy', {'scaling_Lmax': scaling_Lmax, 'inclination_factor': inclination_factor})
    lsys_fet = Lsystem('TD_lsystem_Fetuque.lpy')
    lsys_luz_str = lsys_luz.derive()
    lsys_fet_str = lsys_fet.derive()
    s_luz = lsys_luz.sceneInterpretation(lsys_luz_str)
    s_fet = lsys_fet.sceneInterpretation(lsys_fet_str)
    scene_asso = s_luz + s_fet
    # Visualisation of the association
    scene_out = Scene()

    for shp in scene_asso:
        if shp.id <= 1000:  # Fetuque
            scene_out += Shape(Translated(distance/2, 0, 0, shp.geometry), shp.appearance, id=shp.id)
        else:  # Luzerne
            scene_out += Shape(Translated(-distance/2, 0, 0, shp.geometry), shp.appearance, id=shp.id)

    colored_scene = Calcul_Caribu(scene_out)
    return SceneWidget(colored_scene, size_world=75)
