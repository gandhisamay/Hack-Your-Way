#include<bits/stdc++.h>
using namespace std;
#define forn(i, a, n) for (int i = a; i < n; i++)
#define MAXN 1000000
#define MOD 1000000007
#define int long long
#define tc       int t; cin>>t; while(t--)
#define mp       make_pair
#define Radhe     ios::sync_with_stdio(false);
#define Krishna cin.tie(NULL);
class Node{
public:
string name="Not defined";
bool gender;
bool f;
int age;
string hno;
Node* father=nullptr;
Node *mother=nullptr;
Node *FIL=nullptr;
Node* MIL=nullptr;
Node* spouse;
vector<Node*>neighbours;
vector<Node*> children;
    
    Node(bool F,string Name, bool gen,int Age,string HNo){
        f=F;
        name=Name,
        hno=HNo;
        gender=gen,
        age=Age;
    }

    void setFather(Node* f){
        father=f;
    }

    void setSpouse(Node* s){
        spouse=s;
        s->spouse=this;
    }

    void addChild(Node* c){
        children.push_back(c);
        c->setFather(this);
    }

    void print(){
        if(father)mother=father->spouse;else mother=nullptr;
        if(FIL)MIL=FIL->spouse;else MIL=nullptr;
        cout<<"Name: "<<name<<endl;
        cout<<"H.No.: "<<hno<<endl;
        cout<<"Gender: "<<(gender?"Male":"Female")<<endl;
        cout<<"Age: "<<(age==INT_MAX?"Not defined":to_string(age))<<endl;
        cout<<"Father: "<<(father==nullptr?"Not defined":father->name)<<endl;
        cout<<"Mother: "<<(mother==nullptr?"Not defined":mother->name)<<endl;
        cout<<"Spouse: "<<(spouse==nullptr?"Not defined":spouse->name)<<endl;
        cout<<"Father-in-law: "<<(FIL==nullptr?"Not defined":FIL->name)<<endl;
        cout<<"Mother-in-law: "<<(MIL==nullptr?"Not defined":MIL->name)<<endl;
        cout<<"Children: ";
        if(children.size()){
        for(auto i:children){
           cout<<i->name<<", ";
        }
        cout<<endl;
        }else cout<<"Not defined"<<endl;
        cout<<"Neighbours: ";
        if(neighbours.size()){
        for(auto i:neighbours){
           cout<<i->name<<", ";
        }
        cout<<endl;
        }else cout<<"Not defined"<<endl;
        cout<<endl;
    }

};

vector<Node*> peeps;
unordered_map<string,vector<Node*>>homes;

void getData(){
bool f=0,m=0;
vector<vector<string>> content;
vector<string> row;
string line, word;
string fname="MASTER CSV.CSV";
fstream file (fname, ios::in);
if(file.is_open())
{
while(getline(file, line))
{
row.clear();
stringstream str(line);
while(getline(str, word, ','))
row.push_back(word);
content.push_back(row);
}
}
else
cout<<"Could not open the file\n";
for(int i=1;i<content.size();i++)
{
string name;
bool gender;
bool f;
int age;
string hno;

for(int j=0;j<content[i].size();j++)
{
    if(content[i][j]=="0"){
        continue;
    }
    if(j==0){
        name=content[i][j];
    }else
    if(j==1){
      f=1;
    }else
    if(j==2){
        f=0;
    }else 
    if(j==3){
        continue;
    }else
    if(j==4){
      age=stoi(content[i][j]);
    }else
    if(j==5){
       if(content[i][j]=="MALE")m=1;
       else m=0;
    }else
    if(j==6){
        hno=content[i][j];
    }
}

Node* n=new Node(f,name,m,age,hno);
peeps.push_back(n);
homes[hno].push_back(n);

}
}


void setData(){
    bool f=0,m=0;
vector<vector<string>> content;
vector<string> row;
string line, word;
string fname="MASTER CSV.CSV";
fstream file (fname, ios::in);
if(file.is_open())
{
while(getline(file, line))
{
row.clear();
stringstream str(line);
while(getline(str, word, ','))
row.push_back(word);
content.push_back(row);
}
}
else
cout<<"Could not open the file\n";
for(int i=1;i<content.size();i++)
{
    string name;
bool gender;
bool f;
int age;
string hno;
Node* father=nullptr;
string fana="";

for(int j=0;j<content[i].size();j++)
{
    if(content[i][j]=="0"){
        continue;
    }
    if(j==0){
        name=content[i][j];
    }else
    if(j==1){
      f=1;
      fana=content[i][j];
    }else
    if(j==2){
        f=0;
        fana=content[i][j];
    }else 
    if(j==3){
        continue;
    }else
    if(j==4){
      age=stoi(content[i][j]);
    }else
    if(j==5){
       if(content[i][j]=="MALE")m=1;
       else m=0;
    }else
    if(j==6){
        hno=content[i][j];
    }
}

int c=0;
for(auto I:peeps){
    string a,b,C;
int co=0;
for(int K=0;K<I->name.size();K++){
    if(I->name[K]==' '){
        co++;
        continue;
    }
    if(co==0)
   a.push_back(I->name[K]);
    else if(co==1)
    b.push_back(I->name[K]);
    else if(co==2)
    C.push_back(I->name[K]);
}
string s=a+" "+C;
    if(s==fana){
        c++;
        if(c==2){
            cout<<"Error: Multiple fathers with same name"<<endl;
            // exit(0);
        }

        father=I;
        if(!f){
           peeps[i-1]->setSpouse(I);
        }else{
            peeps[i-1]->setFather(I);
            I->addChild(peeps[i-1]);
        }
    }
}
if(!c){
    if(fana==""){
        continue;
    }
    if(f){
        peeps[i-1]->father=new Node(1,fana,1,INT_MAX,"Not defined");
        peeps[i-1]->father->spouse=nullptr;
        }

    else {
        peeps[i-1]->spouse=new Node(1,fana,1,INT_MAX,"Not defined");
        peeps[i-1]->spouse->setSpouse(peeps[i-1]);
        }
}
}

}




void pruneData(){
    for(int i=0;i<peeps.size();i++){
        if(peeps[i]->father && peeps[i]->father->spouse ){
          peeps[i]->mother=peeps[i]->father->spouse;
            peeps[i]->mother->addChild(peeps[i]);
        }
    }

    for(int i=0;i<peeps.size();i++){
        if(peeps[i]->spouse){
          peeps[i]->FIL=peeps[i]->spouse->father;
          peeps[i]->MIL=peeps[i]->spouse->mother;
        }
    }

    for(int i=0;i<peeps.size();i++){
       for(auto I:homes[peeps[i]->hno]){
           peeps[i]->neighbours.push_back(I);
       }
    }


  
}


void create()
{
	// file pointer
	fstream fout;

	// opens an existing csv file or creates a new file.
	fout.open("Out.csv", ios::out | ios::app);
   fout<<"Name,HNo,Gender,Age,Father,Mother,Spouse,FIL,MIL,Children,Neighbours"<<endl;
	int n=peeps.size();
    for(int i=0;i<n;i++){
        fout<<peeps[i]->name<<","<<peeps[i]->hno<<","<<peeps[i]->gender<<","<<peeps[i]->age<<",";
        if(peeps[i]->father)fout<<peeps[i]->father->name;else fout<<0;
        fout<<",";
        if(peeps[i]->mother)fout<<peeps[i]->mother->name;else fout<<0;
        fout<<",";
        if(peeps[i]->spouse)fout<<peeps[i]->spouse->name;else fout<<0;
        fout<<",";
        if(peeps[i]->FIL)fout<<peeps[i]->FIL->name;else fout<<0;
        fout<<",";
        if(peeps[i]->MIL)fout<<peeps[i]->MIL->name;else fout<<0;
        fout<<",[";
        int z=peeps[i]->children.size();
        if(z)
        {for(int j=0;j<z;j++){
            fout<<peeps[i]->children[j]->name;
            if(j!=z-1)fout<<",";
        }}else{
          fout<<0;
        }

        fout<<"],[";

        z=peeps[i]->neighbours.size();
        if(z)
        {for(int j=0;j<z;j++){
            fout<<peeps[i]->neighbours[j]->name;
            if(j!=z-1)fout<<",";
        }}else{
          fout<<0;
        }

        fout<<"]"<<endl;
    }

	
		// Insert the data to file
		
	}







int32_t main(){
Radhe Krishna


getData();
setData();
pruneData();
create();
// for(auto i:peeps){
//     i->print();
// }

int n=peeps.size();
// cout<<n<<endl;
for(int i=0;i<n;i++){
    cout<<i<<endl;
    peeps[i]->print();
}

return 0;
}
