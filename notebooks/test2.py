from jupyros import RosBag

bag = RosBag('bags/pallet.bag')
#bag
#bag.show_types()
#bag.show_topics()
display(bag.ui())
bag.play()