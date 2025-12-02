import signac

import ovito
from ovito.io import import_file, export_file
from ovito.modifiers import ConstructSurfaceModifier, SelectTypeModifier, DeleteSelectedModifier, WrapPeriodicImagesModifier 
from ovito.vis import SurfaceMeshVis, Viewport




def construct_image(job, pipeline):
    topo_file = "lmp_data/equil.data"
    assert job.isfile(topo_file)

    pipeline.source.load(job.path + '/' + topo_file)

    # Surface Construction
    vp = Viewport()
    vp.type = Viewport.Type.Front

    data = pipeline.compute() 
    data.particles.vis.radius = 0.45
    pipeline.add_to_scene()



    # Render view
    vp.zoom_all()
    vp.render_image(filename = f"{job.path}/figs/equil_surface_r1.5.png") 


if __name__ == "__main__":
    project = signac.get_project()

    job1 = project.open_job(id = '142994160ca38e51087d13a69ae586fd')
    topo_file = job1.path + "/lmp_data/equil.data"
    pipeline = import_file(topo_file)
    surface_mod = ConstructSurfaceModifier(
            method = ConstructSurfaceModifier.Method.AlphaShape,
            radius = 1.5
            )
    surface_vis = SurfaceMeshVis(
            clip_at_domain_boundaries = True,
            reverse_orientation = True,
            enabled = True
            )
    
    surface_mod.vis = surface_vis
    # Select and Delete polymers from view
    select_mod = SelectTypeModifier(
            operate_on = 'particles',
            property = 'Particle Type',
            types = {'Type 1', 'Type 2'},
            enabled = True
            )
    pipeline.modifiers.append(surface_mod)
    pipeline.modifiers.append(select_mod)
    pipeline.modifiers.append(DeleteSelectedModifier())
    for job in project:
        construct_image(job, pipeline)
    
    # job = project.open_job(id=job_id)
    # construct_image(job)
