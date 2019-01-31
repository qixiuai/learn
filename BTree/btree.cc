
#include <iostream>

using namespace std;

class BTreeNode {
  int* keys;
  int t;
  BTreeNode** C;
  int n;
  bool leaf;
public:
  BTreeNode(int _t, bool _leaf);

  void traverse();

  BTreeNode* search(int k);

  friend class BTree;
};

class BTree {
  BTreeNode* root;
  int t;
public:
  BTree(int _t) {
    root = NULL;
    t = _t;
  }
  
  void traverse() {
    if (root != NULL)
      root->traverse();
  }
  
  BTreeNode* search(int k) {
    return (root == NULL) ? NULL : root->search(k);
  }
};


