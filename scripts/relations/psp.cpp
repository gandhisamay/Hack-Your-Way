#include <bits/stdc++.h>
using namespace std;
#define forn(i, a, n) for (int i = a; i < n; i++)
#define MAXN 1000000
#define MOD 1000000007
#define int long long
#define tc    \
    int t;    \
    cin >> t; \
    while (t--)
#define mp make_pair
#define Radhe ios::sync_with_stdio(false);
#define Krishna cin.tie(NULL);

// class Tree{
//     public:
//     unordered_set<string> s;

// };

class Node
{
public:
    string name, voterID;
    bool gender;
    bool f;
    int age;
    Node *father = nullptr;
    // *mother=nullptr,*husband=nullptr;
    vector<Node *> spouse;
    vector<Node *> children;

    Node(bool F, string Name, string vID, bool gen, int Age)
    {
        f = F;
        name = Name,
        voterID = vID,
        gender = gen,
        age = Age;
    }

    void setFather(Node *f)
    {
        father = f;
    }

    void addSpouse(Node *s)
    {
        spouse.push_back(s);
        s->setFather(this);
        s->spouse.push_back(this);
    }

    void addChild(Node *c)
    {
        children.push_back(c);
        c->setFather(this);
    }

    void print()
    {
        cout << "Name: " << name << endl;
        cout << "Voter ID: " << voterID << endl;
        cout << "Gender: " << (gender ? "Male" : "Female") << endl;
        cout << "Age: " << age << endl;
        cout << (f ? "Father: " : "Husband: ") << (father == nullptr ? "Not defined" : father->name) << endl;

        if (gender && spouse.size())
        {
            cout << "Spouse: ";
            for (auto i : spouse)
            {
                i->print();
            }
            cout << endl;
        }
        if (children.size())
        {
            cout << "Children: ";
            for (auto i : children)
            {
                i->print();
            }
            cout << endl;
        }

        cout << endl;
    }

    void tree_print(int x)
    {
        // cout<<endl;
        for (int i = 0; i < x + 4; i++)
        {
            cout << " ";
        }
        cout << "-->" << name << " ";

        if (spouse.size())
        {
            cout << "---";
            for (auto i : spouse)
            {

                cout << " " << i->name;
                // cout<<", ";
            }
        }

        cout << endl;

        if (gender)
        {
            // cout<<"PSP"<<endl;
            if (children.size())
            {

                for (int i = 0; i < (x + 5); i++)
                {
                    cout << " ";
                }
                cout << "|" << endl;
                for (auto i : children)
                {
                    i->tree_print(x + 1);
                }
                // cout<<endl;
            }
        }

        else
        {

            if (spouse.size() && spouse[0]->children.size())
            {

                for (int i = 0; i < (x + 5); i++)
                {
                    cout << " ";
                }
                cout << "|" << endl;
                for (auto i : spouse[0]->children)
                {
                    i->tree_print(x + 1);
                }
                // cout<<endl;
            }
        }

        // cout<<endl;
    }
};

vector<Node *> peeps;

// void getData(){
//     bool f=0,m=0;
// if(checkf())f=1;
// if(checkm())m=1;
// peeps.push_back(new Node(f,"Rajesh","123",m,40));
// }

// void solve(){
//         Node* father=find(father);
//         if(father){
//             if(checkf()){
//         father->addChild(this);
//                 }else{
//                     father->addSpouse(this);
//                  }
//         }

// }

// Node* find(Node *c){
//     if(c->f){
//         for(auto i:peeps){
//         if(i->name==name && i->age>c->age)return i;
//     }

//     }else{
//         for(auto i:peeps){
//         if(i->name==name)return i;
//     }

//     }

//     return nullptr;
// }

int32_t main()
{
    Radhe Krishna
        Node *a = new Node(1, "Rajesh", "123", 1, 40);
    Node *b = new Node(0, "Popli", "123", 0, 40);
    Node *c = new Node(1, "Rajesha", "123", 1, 40);
    Node *d = new Node(0, "Rajeshi", "123", 0, 40);
    Node *e = new Node(1, "Lajesh", "123", 1, 40);
    Node *f = new Node(0, "Lajo", "123", 0, 40);
    Node *g = new Node(1, "Lajeshi", "123", 1, 40);
    Node *h = new Node(0, "Lajeshii", "123", 0, 40);
    Node *i = new Node(1, "Lajeshiii", "123", 1, 40);
    Node *j = new Node(0, "Lajeshiiii", "123", 0, 40);
    Node *k = new Node(1, "Lajeshiiiii", "123", 1, 40);
    Node *l = new Node(0, "Lajeshiiiiii", "123", 0, 40);
    Node *m = new Node(1, "Prajesh", "123", 1, 40);
    Node *n = new Node(0, "Peepa", "123", 0, 40);
    e->addSpouse(f);
    a->addSpouse(b);
    c->addSpouse(d);
    g->addSpouse(h);
    i->addSpouse(j);
    k->addSpouse(l);
    // m->addSpouse(n);

    a->addChild(c);
    c->addChild(e);
    c->addChild(g);
    c->addChild(m);
    c->addChild(n);
    g->addChild(i);
    g->addChild(k);

    // Node* gf=new Node(true,"Rajesh","123",true,40);
    // gf->addChild(new Node(true,"Raesh","1231",true,4));
    // gf->addChild(new Node(true,"Rajiniesh","12312",false,8));
    // Node* Gum=new Node(false,"Reri","10213",false,50);
    // Node* Mum=new Node(false,"Rajeshwari","1213",false,40);
    // gf->addSpouse(Mum);
    // Node *f=new Node(true,"Raku","12113",true,37);
    // f->addSpouse(Gum);
    // f->addSpouse(Mum);
    // gf->addChild(f);
    // f->addChild(new Node(true,"Lodesh","12s312",false,19));

    a->tree_print(0);

    // getData();
    return 0;
}
