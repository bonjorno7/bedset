## Bedset

### Some tools to make Blender more comfortable

#### Pie menus
Press B to open the Bedset pie, you can figure it out from there.

#### Edges

* Select: select edges that meet the set criteria (seam, sharp, bevel, crease, angle)
* Select Inverted: select edges that **don't** meet the criteria (seam, sharp, bevel, crease, any)
* Mark: mark edges as seam, sharp, bevel, crease
* Clear: clear edges of seam, sharp, bevel, crease, all

#### Booleans in object mode

* Difference
* Union
* Intersect
* Apply: applies all modifiers on selected objects

I'm working on adding Slice and Inset next.

#### Booleans in edit mode

* Difference
* Union
* Intersect
* Cut: uses the cutter like a knife

#### Modifiers

* Bevel
* Solidify

I'm still thinking about which modifiers to add next, since I want to keep it minimal.

#### Other

* Auto Smooth: smooth the object and enable auto smooth with the specified angle
* Export Obj: export each selected object to a .obj, you have to save the project first

#### Baking

I added PBR baking a while ago but didn't end up using it. You can find the panel in the Bedset tab, in the list of tabs that appears when you press N in the 3D view.
