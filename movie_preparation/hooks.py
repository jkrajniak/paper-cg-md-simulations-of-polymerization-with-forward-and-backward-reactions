

def hook_at_step(system, integrator, ar, gt, args, k):
    if k == 0:
        print('Deactivation reaction 2 3')
        ar.get_reaction(2).active = False
        ar.get_reaction(3).active = False
    if k == 1000000:
        print('Deactivate reactions 0, 1')
        ar.get_reaction(0).active = False
        ar.get_reaction(1).active = False
        ar.get_reaction(2).active = True
        ar.get_reaction(3).active = True
