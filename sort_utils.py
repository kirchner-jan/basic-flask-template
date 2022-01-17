# imports
from sentence_transformers import SentenceTransformer, util
from anytree.importer import JsonImporter
from anytree.exporter import JsonExporter
from anytree import PreOrderIter, PostOrderIter
from tqdm import tqdm
import numpy as np
from textscoring import model
import dill, nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def load_tree(inPath):
  with open(inPath) as f:
    root = importer.read(f)
  return root

def get_gramm_model(gramm_path):
  with open(gramm_path, 'rb') as file:
    gramm_model = dill.load(file)
  return gramm_model

def add_g_rating(root , gramm_model):
  for node in tqdm(PreOrderIter(root , filter_= lambda n: not hasattr(n , 'g_rating'))):
    node.g_rating = gramm_model.rate(node.name)/10.

def add_s_rating(root , sci_model):
  refEMB = sci_model.encode([root.name])
  for node in tqdm(PreOrderIter(root , filter_= lambda n: not hasattr(n , 's_rating'))):
    cEMB = sci_model.encode([node.name])
    node.s_rating = float(util.cos_sim(refEMB, cEMB).detach().numpy().squeeze())

def add_t_rating(root):
  for node in PreOrderIter(root , filter_= lambda n: not hasattr(n , 't_rating')):
    node.t_rating = np.sqrt(node.s_rating**2 + node.g_rating**2)

def add_r_rating(root):
  for node in PostOrderIter(root):
    t_ratings = [x.t_rating for x in node.children]
    node.r_rating = 0.25*np.max(t_ratings) + 0.75*node.t_rating if len(t_ratings) > 0 else node.t_rating

def sort_by_r(root):
  for node in PreOrderIter(root):
    r_ratings = [x.r_rating for x in node.children]
    node.children = [x for _, x in sorted(zip(r_ratings, node.children))]

def save_tree(outPath , root):
  with open(outPath , 'w') as f:
      exporter.write(root, f)

def sort_tree(inPath , outPath):
  importer , exporter = JsonImporter() , JsonExporter(indent=2, sort_keys=False)
  print('Loading tree...')
  root = load_tree(inPath)
  print('Loading grammar model...')
  gramm_model = get_gramm_model(r"textscoring/training/model.dill")
  print('Adding grammar score...')
  add_g_rating(root , gramm_model)
  print('Adding semantic similarity score...')
  sci_model = SentenceTransformer('all-mpnet-base-v2')
  add_s_rating(root , sci_model)
  print('Computing total similarity score...')
  add_t_rating(root)
  print('Computing recursive similarity score...')
  add_r_rating(root)
  print('Sorting by total similarity score...')
  sort_by_r(root)
  print('Saving tree...')
  save_tree(outPath , root)
  