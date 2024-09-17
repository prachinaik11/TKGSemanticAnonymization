import pymoo
import numpy as np
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
import pandas as pd
from pymoo.util.plotting import plot

def get_values_for_snapshot_id(csv_file):
  # Read CSV data into a DataFrame
  df = pd.read_csv(csv_file)

  # Initialize lists to store values for each snapshot ID
  AIL_values = []
  final_SE_similarity_values = []
  final_SA_similarity_values = []

  # Group data by snapshot_id
  grouped = df.groupby('snapshot_id')

  # Iterate over groups and extract values
  for snapshot_id, group in grouped:
    AIL_values.append(group['AIL'].tolist())
    final_SE_similarity_values.append(group['final_SE_similarity'].tolist())
    final_SA_similarity_values.append(group['final_SA_similarity'].tolist())

  return AIL_values, final_SE_similarity_values, final_SA_similarity_values

# csv_file = "extracted_values.csv"  # Replace with your CSV file path
# AIL_values, final_SE_similarity_values, final_SA_similarity_values = get_values_for_snapshot_id(csv_file)
#
# # Example printing the first few values of each list
# print("AIL values for each snapshot ID:")
# print(AIL_values[0])
# print("\nfinal_SE_similarity values for each snapshot ID:")
# print(final_SE_similarity_values)
# print("\nfinal_SA_similarity values for each snapshot ID:")
# print(final_SA_similarity_values)

class MyProblem(Problem):
# For minimising SE distances
    def __init__(self):
      super().__init__(n_var=2, n_obj=3, n_ieq_constr = 0, xl=np.array([2, 1]), xu=np.array([10, 4]), vtype=int)

    def _evaluate(self, x, out, *args, **kwargs):
      # for SE similarity
      obj1 = -1 * fun1(x[:,0], x[:,1])
      # for SA similarity
      obj2 = fun2(x[:,0], x[:,1])
      # for information loss
      obj3 = fun3(x[:,0], x[:,1])
      # constr = x[:,1] - x[:,0]

      out["F"] = np.column_stack([obj1, obj2, obj3])

      # out["G"] = np.column_stack([constr])

# for SE similarity -- maximising
def fun1(k, l):
  csv_file = "extracted_values.csv"  # Replace with your CSV file path
  AIL_values, final_SE_similarity_values, final_SA_similarity_values = get_values_for_snapshot_id(csv_file)
  distances1 = final_SE_similarity_values[0]
  print(distances1)
  print("fun1 k = ",k)
  print("l = ",l)
  print(type(k))
  # distances1 = [0.7112, 0.6918, 0.6488, 0.6414, 0.6118, 0.6122, 0.6028, 0.5861, 0.7188, 0.6970, 0.6461, 0.6474, 0.6228, 0.6130, 0.5945, 0.5865, 0.7159, 0.6964, 0.6552, 0.6497, 0.6154, 0.6096, 0.6019, 0.5924, 0.7486, 0.7013, 0.6509, 0.6438, 0.6033, 0.6057, 0.5997, 0.5877]

  count = 0
  m = 0
  dict1 = {}
  for i in (1,2,3,4):
      for j in (2,4,6,8,10):
        count = count+1
        if j >= i:
          dict1[str(j)+','+str(i)] = distances1[m]
        else:
          dict1[str(j)+','+str(i)] = 0
        m = m + 1
  print("dict1 : ",dict1)
  print("count : ",count)

  out = np.empty(len(k))
  print("out: ",out)

  for i in range(0, len(k)):
    print(str(k[i])+','+str(l[i]))
    if str(k[i])+','+str(l[i]) in dict1:
      out[i] = dict1[str(k[i])+','+str(l[i])]
    else:
      out[i] = 0
  print("distances1 : ",distances1)
  print("out : ",out)
  return out

# for SA similarity -- minimising
def fun2(k, l):
  csv_file = "extracted_values.csv"  # Replace with your CSV file path
  AIL_values, final_SE_similarity_values, final_SA_similarity_values = get_values_for_snapshot_id(csv_file)
  distances2 = final_SA_similarity_values[0]
  print("fun2 k = ",k)
  print("l = ",l)
  # distances2 = [0.5152, 0.5106, 0.5134, 0.5157, 0.5133, 0.5180, 0.5141, 0.5147, 0.5150, 0.5109, 0.5135, 0.5127, 0.5145, 0.5130, 0.5110, 0.5152, 0.5121, 0.5123, 0.5107, 0.5091, 0.5148, 0.5105, 0.5165, 0.5136, 0.5092, 0.5115, 0.5119, 0.5140, 0.5156, 0.5105, 0.5137, 0.5126]

  m = 0
  dict1 = {}
  for i in (1,2,3,4):
      for j in (2,4,6,8,10):
        if j >= i:
          dict1[str(j)+','+str(i)] = distances2[m]
        else:
          dict1[str(j)+','+str(i)] = 1
        m = m + 1
  print("dict1 : ",dict1)

  out = np.empty(len(k))
  print("out: ",out)

  for i in range(0, len(k)):
    print(str(k[i])+','+str(l[i]))
    if str(k[i]) + ',' + str(l[i]) in dict1:
      out[i] = dict1[str(k[i])+','+str(l[i])]
    else:
      out[i] = 1
  print("distances2 : ",distances2)
  print("out : ",out)
  return out


# for information loss -- minimising
def fun3(k, l):
  csv_file = "extracted_values.csv"  # Replace with your CSV file path
  AIL_values, final_SE_similarity_values, final_SA_similarity_values = get_values_for_snapshot_id(csv_file)
  distances2 = AIL_values[0]
  print("fun2 k = ",k)
  print("l = ",l)
  # distances2 = [0.2016495185575782, 0.1787935739469469, 0.19882846526380107, 0.18374794363038102, 0.19950071605613048, 0.20544363532182683, 0.18686886316590365, 0.19122544655614582, 0.2058664992588875, 0.18423641104786503, 0.17457116889843752, 0.18534439133756403, 0.19060236945567713, 0.18886970996475297, 0.19970861079629068, 0.17373446122763758, 0.20949942469958538, 0.18640564471879092, 0.19003645023537113, 0.19366039062638746, 0.2028358771723151, 0.19093186412720398, 0.21434311915238732, 0.20522591183684913, 0.31345135266473717, 0.18412863310704838, 0.20503201826738446, 0.18536079302496272, 0.2076846296364811, 0.18882599526151198, 0.2033354066926929, 0.16959007260233708]

  m = 0
  dict1 = {}
  for i in (1,2,3,4):
      for j in (2,4,6,8,10):
        if j >= i:
          dict1[str(j)+','+str(i)] = distances2[m]
        else:
          dict1[str(j)+','+str(i)] = 1
        m = m + 1
  print("dict1 : ",dict1)

  out = np.empty(len(k))
  print("out: ",out)

  for i in range(0, len(k)):
    print(str(k[i])+','+str(l[i]))
    if str(k[i]) + ',' + str(l[i]) in dict1:
      out[i] = dict1[str(k[i])+','+str(l[i])]
    else:
      out[i] = 1
  print("distances2 : ",distances2)
  print("out : ",out)
  return out


problem = MyProblem()
algorithm = NSGA2(pop_size=100,
            sampling=IntegerRandomSampling(),
            crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
            mutation=PM(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
            eliminate_duplicates=True,
               )

res = minimize(problem,
               algorithm,
               termination=('n_gen', 100),
               seed=1,
               save_history=True,
               verbose = False)

print(res.X)
print(res.F)

plot(res.X, no_fill=True)
plot(res.F)