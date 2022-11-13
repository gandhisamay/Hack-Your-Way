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
int gender;
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
    
    Node(bool F,string Name, int gen,int Age,string HNo){
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

        cout<<"Gender: ";
        if(gender==1)cout<<"MALE"<<endl;
        else if(gender==2)cout<<"UNDEFINED"<<endl;
        else cout<<"FEMALE"<<endl;

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
bool f=0;int m=0;
vector<vector<string>> content;
vector<string> row;
string line, word;
// string fname="../txt_to_csv/output.csv";
string fname="test_undefined.csv";
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
int gender;
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
        // cout<<content[i][j]<<endl;
      age=stoi(content[i][j]);
    }else
    if(j==5){
       if(content[i][j]=="OTHERS"||content[i][j]=="UNDEFINED")m=2;
       else if(content[i][j]=="MALE")m=1;
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
    bool f=0;int m=0;
vector<vector<string>> content;
vector<string> row;
string line, word;
// string fname="../txt_to_csv/output.csv";
string fname="test_undefined.csv";

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
int gender;
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
        // cout<<content[i][j]<<endl;
      age=stoi(content[i][j]);
    }else
    if(j==5){
      if(content[i][j]=="OTHERS"||content[i][j]=="UNDEFINED")m=2;
       else if(content[i][j]=="MALE")m=1;
       else m=0;
    }else
    if(j==6){
        hno=content[i][j];
    }
}

int c=0;
for(auto I:peeps){
    string temp=I->name;
    int sp=0;
    for(auto x:temp){
        if(x==' ')sp++;
    }

string s=I->name;
if(sp>1){
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
s=a+" "+C;
}
    if(s==fana){
        c++;
        if(c==2){
            cout<<"Error: Multiple fathers with same name: "<<s<<" "<<I->name<<endl;
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



// cout<<"------------------------------------------------------------------------------------------------------------------------"<<endl;
//     for(auto x:homes){
//         cout<<x.first<<" : ";
//         for(auto y:x.second){
//             cout<<y->name<<" ";
//         }
//         cout<<endl;
//     }

// cout<<"------------------------------------------------------------------------------------------------------------------------"<<endl;


    for(int i=0;i<peeps.size();i++){
       for(auto I:homes[peeps[i]->hno]){
           peeps[i]->neighbours.push_back(I);
       }
    }


  
}


void create(string name, string f, string Fname, string age)
{
	// file pointer
	fstream fout;

	// opens an existing csv file or creates a new file.
	fout.open("Out.csv", ios::out | ios::app);
   fout<<"Name,HNo,Gender,Age,Father,Mother,Spouse,FIL,MIL,Children,Neighbours"<<endl;
	int n=peeps.size();
    
    for(int i=0;i<n;i++){
        if(peeps[i]->name!=name || (f=="1")&& peeps[i]->father && peeps[i]->father->name!=Fname || (f=="0")&& peeps[i]->spouse && peeps[i]->spouse->name!=Fname ||  peeps[i]->age!=stoi(age)){
                continue;
        }
        fout<<peeps[i]->name<<","<<peeps[i]->hno<<",";
        if(peeps[i]->gender==1)fout<<"MALE";
        else if(peeps[i]->gender==2)fout<<"UNDEFINED";
        else fout<<"FEMALE";
        fout<<","<<peeps[i]->age<<",";
        if(peeps[i]->father)fout<<peeps[i]->father->name;else fout<<0;
        fout<<",";
        if(peeps[i]->mother)fout<<peeps[i]->mother->name;else fout<<0;
        fout<<",";
        if(peeps[i]->spouse)fout<<peeps[i]->spouse->name;else fout<<0;
        fout<<",";
        if(peeps[i]->FIL)fout<<peeps[i]->FIL->name;else fout<<0;
        fout<<",";
        if(peeps[i]->MIL)fout<<peeps[i]->MIL->name;else fout<<0;
        fout<<",";
        int z=peeps[i]->children.size();
        if(z)
        {for(int j=0;j<z;j++){
            fout<<peeps[i]->children[j]->name;
            if(j!=z-1)fout<<"|";
        }}else{
          fout<<0;
        }

        fout<<",";

        z=peeps[i]->neighbours.size();
        if(z)
        {for(int j=0;j<z;j++){
            fout<<peeps[i]->neighbours[j]->name;
            if(j!=z-1)fout<<"|";
        }}else{
          fout<<0;
        }

        fout<<""<<endl;
    }

	
		// Insert the data to file
		
	}



    void createJson(string name, string f, string Fname, string age)
{
	// file pointer
	fstream fout;

	// opens an existing csv file or creates a new file.
	fout.open("Out.json", ios::out | ios::app);
    fout<<"{"<<endl;

//    fout<<"Name,HNo,Gender,Age,Father,Mother,Spouse,FIL,MIL,Children,Neighbours"<<endl;
	int n=peeps.size();
    for(int i=0;i<n;i++){
        if(peeps[i]->name!=name || (f=="1")&& peeps[i]->father && peeps[i]->father->name!=Fname || (f=="0")&& peeps[i]->spouse && peeps[i]->spouse->name!=Fname ||  peeps[i]->age!=stoi(age)){
                continue;
        }
        fout<<"\""<<i<<"\""<<":{"<<endl;
        fout<<"\"Name\""<<":"<<"\""<<peeps[i]->name<<"\""<<","<<endl;
        fout<<"\"HNo\""<<":"<<"\""<<peeps[i]->hno<<"\""<<","<<endl;
        fout<<"\"Gender\""<<":"<<"\"";
        if(peeps[i]->gender==1)fout<<"MALE";
        else if(peeps[i]->gender==2)fout<<"UNDEFINED";
        else fout<<"FEMALE";
        fout<<"\""<<","<<endl;
        fout<<"\"Age\""<<":"<<"\""<<peeps[i]->age<<"\""<<","<<endl;
        fout<<"\"Father\""<<":"<<"\""<<(!(peeps[i]->father)?"_Not_defined_":peeps[i]->father->name)<<"\""<<","<<endl;
        fout<<"\"Mother\""<<":"<<"\""<<(!(peeps[i]->mother)?"_Not_defined_":peeps[i]->mother->name)<<"\""<<","<<endl;
        fout<<"\"Spouse\""<<":"<<"\""<<(!(peeps[i]->spouse)?"_Not_defined_":peeps[i]->spouse->name)<<"\""<<","<<endl;
        fout<<"\"FIL\""<<":"<<"\""<<(!(peeps[i]->FIL)?"_Not_defined_":peeps[i]->FIL->name)<<"\""<<","<<endl;
        fout<<"\"MIL\""<<":"<<"\""<<(!(peeps[i]->MIL)?"_Not_defined_":peeps[i]->MIL->name)<<"\""<<","<<endl;
        fout<<"\"Children\""<<":";
        int z=peeps[i]->children.size();
        if(z==0){
            fout<<"\"_Not_defined_\"";
        }else{
            fout<<"[";
            for(int j=0;j<z;j++){
            fout<<"\""<<peeps[i]->children[j]->name<<"\"";
            if(j!=z-1)fout<<",";

        }
        fout<<"]";

        }
        fout<<","<<endl;
        fout<<"\"Neighbours\""<<":";
        z=peeps[i]->neighbours.size();
        if(z==0){
            fout<<"\"_Not_defined_\"";
        }else{
            fout<<"[";
            for(int j=0;j<z;j++){
            fout<<"\""<<peeps[i]->neighbours[j]->name<<"\"";
            if(j!=z-1)fout<<",";

        }
        fout<<"]"<<endl;

        }

        fout<<"}";
        if(i!=n-1)fout<<","<<endl;
    }

	

    fout<<"}"<<endl;

		// Insert the data to file
		
	}







int32_t main(int32_t argc, char **argv){
Radhe Krishna


getData();
setData();
pruneData();
create(argv[1],argv[2],argv[3],argv[4]);

// createJson(argv[1],argv[2],argv[3],argv[4]);
// for(auto i:peeps){
//     i->print();
// }

int n=peeps.size();
// cout<<n<<endl;
// string a=arg[4];
for(int i=0;i<n;i++){
    if(peeps[i]->name!=argv[1] || (argv[2]=="1")&& peeps[i]->father && peeps[i]->father->name!=argv[3] || (argv[2]=="0")&& peeps[i]->spouse && peeps[i]->spouse->name!=argv[3] ||  peeps[i]->age!=stoi(argv[4])){
                continue;
        }
    cout<<i<<endl;
    peeps[i]->print();
}

return 0;
}
