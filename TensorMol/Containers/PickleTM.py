from __future__ import absolute_import
#kan
from ..Util import *
#kan
import pickle,sys
if sys.version_info > (3, 0):
	import copyreg
else:
	import copy_reg

renametable = {
	'TensorMol.TensorMolData_EE': 'TensorMol.TensorMolDataEE',
	'TensorMol.TFMolInstance_EE': 'TensorMol.TFMolInstanceEE',
	'TensorMol.TensorMolData': 'TensorMol.Containers.TensorMolData',
	'TensorMol.Mol': 'TensorMol.Containers.Mol',
	'TensorMol.Sets': 'TensorMol.Containers.Sets',
	'DigestMol': 'TensorMol.Containers.DigestMol',
	'TensorMol.DigestMol': 'TensorMol.Containers.DigestMol',
	'TensorMol.TFMolInstanceDirect': 'TensorMol.TFNetworks.TFMolInstanceDirect',
	'TensorMol.Transformer': 'TensorMol.ForceModifiers.Transformer',
	'TensorMolData_EE': 'TensorMolDataEE'
	}

def PickleMapName(name):
	"""
	If you change the name of a function or module, then pickle, you can fix it with this.
	"""
	if name in renametable:
		#print("REMAPPING PICKLE LOAD:",name,"TO",renametable[name])
		return renametable[name]
	#else:
	#	print("NOT REMAPPING PICKLE LOAD:",name)
	return name

def mapped_load_global(self):
	module = PickleMapName(self.readline()[:-1])
	name = PickleMapName(self.readline()[:-1])
	#kan
	#print("Finding ", module,name)
	LOGGER.debug("Containers: mapped_load_global: found "+module+' '+name)
	#kan
	klass = self.find_class(module, name)
	self.append(klass)

class MyUnpickler(pickle.Unpickler):
	def find_class(self, module, name):
		return pickle.Unpickler.find_class(self,PickleMapName(module),PickleMapName(name))

def UnPickleTM(file):
	"""
	Eventually we need to figure out how the mechanics of dispatch tables changed.
	Since we only use this as a hack anyways, I'll just comment out what changed
	between python2.7x and python3x.
	"""
	tmp = None
	if sys.version_info[0] < 3:
		f = open(file,"rb")
		unpickler = pickle.Unpickler(f)
		unpickler.dispatch[pickle.GLOBAL] = mapped_load_global
		tmp = unpickler.load()
		f.close()
	else:
		f = open(file,"rb")
		#kan unpickler = MyUnpickler(f,encoding='latin1')
		#kan tmp = unpickler.load()
		#kan f.close()
		try:
			unpickler = MyUnpickler(f,encoding='latin1')
			tmp = unpickler.load()
		except EOFError:
			f.close()
			return tmp
	tmp.pop('evaluate',None)
	tmp.pop('MolInstance_fc_sqdiff_BP',None)
	tmp.pop('Eval_BPForceSingle',None)
	tmp.pop('TFMolManage',None)
	tmp.pop('TFManage',None)
	tmp.pop('Prepare',None)
	tmp.pop('load',None)
	tmp.pop('Load',None)
	tmp.pop('TensorMol.TFMolManage.path',None)
	tmp.pop('TensorMol.TFMolManage.Load',None)
	tmp.pop('TensorMol.TFMolManage.Prepare',None)
	tmp.pop('TensorMol.TFInstance',None)
	tmp.pop('TensorMol.TFInstance.train_dir',None)
	tmp.pop('TensorMol.TFMolInstance.train_dir',None)
	tmp.pop('TensorMol.TFInstance.chk_file',None)
	tmp.pop('TensorMol.TFMolInstance.chk_file',None)
	tmp.pop('save',None)
	tmp.pop('Save',None)
	tmp.pop('Trainable',None)
	tmp.pop('TFMolManage.Trainable',None)
	tmp.pop('__init__',None)
	return tmp
