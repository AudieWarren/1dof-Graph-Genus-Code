# this is a probabilistic Maple program for computing the starting point on a generic tropical fiber
# the graph is given by a list of edges
# the output consists of two partitions, Xpart and Ypart,
# induced by the value function. The subsets in the partition are ordered,
# so for instance if the output is Xpart := [[0,1,2],[3],[4],[5]] then the minimum is
# obtained at 0,1,2, and the value at 5 is largest.

# the algorithm is "Las Vegas" - if it returns a starting point, then we get points of X and Y
# on maximal faces that intersect transversally.

with(GraphTheory):
with(ListTools):

# Random integer between -n and n
Randi := proc(n)
  local arb;
  # random integer
  arb := rand(-n..n);
  arb();
end proc:

# read edges from infile
#edges := [[0,1],[0,2],[0,3],[1,5],[2,5],[3,5]]:
read(infile):

# build a Maple graph and compute a spanning tree
n := nops(edges):
revedges := map(T->[T[2],T[1]],edges):
setedges := map(T->{T[1],T[2]},edges):
graph := Graph({op(setedges)}):
sptree := SpanningTree(graph):

# the variables
var :=    {seq(x[r],r=1..n),seq(y[r],r=1..n)}:
varvec := [seq(x[r],r=1..n),seq(y[r],r=1..n)]:

# the cycle equations (only for a cycle bases)
Ceqs := x[1]-1,y[1]-1: # norming equations
for r to n do
  i,j := op(edges[r]):
  if not ({i,j} in Edges(sptree)) then
    # any edge outside sptree plus the shortest path gives a cycle
    path := ShortestPath(sptree,i,j):
    eqx, eqy := -x[r],-y[r]:
    for k to nops(path)-1 do
      p,q := path[k],path[k+1]:
      edi := Search([p,q],edges):
      if edi > 0 then
        eqx := eqx+x[edi]:
        eqy := eqy+y[edi]:
      else 
        edi := Search([p,q],revedges):
        eqx := eqx-x[edi]:
        eqy := eqy-y[edi]:
      fi:
    od:
  Ceqs := Ceqs,eqx,eqy:
  fi:
od:
Ceqs := {Ceqs}:

# The random equations (exponents between -10n and 10n)
Reqs := {seq(x[r]*t^Randi(10*n)-y[r],r=2..n),x[n]-t^Randi(10*n)}:

# get exponents for the solution
sol := subs(solve({op(Ceqs),op(Reqs)},var),varvec):
vals := map(T->ldegree(numer(T))-ldegree(denom(T)),sol):
xvals := vals[1..n]:
yvals := vals[n+1..2*n]:

# get ordered values
xset := {op(xvals)}:
yset := {op(yvals)}:
xsteps := sort([op(xset)]):
ysteps := sort([op(yset)]):

if (nops(xset) = n/2+1 and nops(yset) = n/2+1) then
  Xpart := map(T->[SearchAll(T,xvals)],xsteps):
  Ypart := map(T->[SearchAll(T,yvals)],ysteps):
# python starts counting with 0 and Maple starts with 1,
# so we need to subtract 1)
  Xpart := map(T->map(S->S-1,T),Xpart):
  Ypart := map(T->map(S->S-1,T),Ypart):
  save(Xpart,Ypart,outfile);
else
  print("error - face may be nonmaximal");
fi;