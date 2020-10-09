#include <iostream>
#include <time.h>

#define WIDTH 15
#define HEIGHT 15
#define WHITE 1 //default computer
#define BLACK 0 //default player
#define BLANK -1
#define DEPTH 4
#define WIN 1
#define LOSE -1
#define TIE 0
#define UNSETTLED 2

typedef struct point {
    int x;
    int y;
}point;

point* createPoint(int x, int y){
    auto* temp= (point *)(malloc(sizeof(point)));
    temp->x=x;
    temp->y=y;
    return temp;
}

typedef struct tree {
    point* node;
    int value;
    tree *next;
    tree *adj;
} tree;

typedef struct list{
    point* node;
    list *next;
} list;

typedef struct stack{
    point* node;
    stack* above;
} stack;

void push(stack* bottom, point* node){
    stack* p=bottom;
    while(p->above!= nullptr){
        p=p->above;
    }
    p->above->node=node;
    p->above->above= nullptr;
}

void pop(stack* bottom){
    stack* p=bottom;
    while(p->above->above!= nullptr){
        p=p->above;
    }
    free(p->above);
    p->above= nullptr;
}

void createNode(list* A, point* node);
void deleteNode(list* A, point* node);
int countList(list* A);
list* searchPoint(int ChessBoard[HEIGHT][WIDTH]);
void createTree(int ChessBoard[HEIGHT][WIDTH], list* nodeList, tree *treeNode, int depth);
int valuePoint(int ChessBoard[HEIGHT][WIDTH], list* nodeList);
tree * createAdjTreeNode(tree* B, point* node);

void createNode(list* A, point* node){
    list* p=A;
    while(p->next!=nullptr){
        p=p->next;
    }
    auto temp= (list *)(malloc(sizeof(list)));
    //A->node->x+=1;
    temp->node=node;
    temp->next=nullptr;
}

void deleteNode(list* A, point* node){
    list* p=A;
    while(p->next->node!=node){
        p=p->next;
    }
    //A->node->x-=1;
    list* temp=p->next;
    p->next=p->next->next;
    free(temp);
}

int countList(list* A){
    int i=0;
    list* p=A;
    while(p->next!=nullptr){
        i++;
    }
    return i+1;
}

int whoIsPlay(int depth){
    if(depth%2==1){
        return BLACK;
    }else{
        return WHITE;
    }
}

list* searchPoint(int ChessBoard[HEIGHT][WIDTH]){
    int searchXMin=0,searchYMin=0,searchXMax=INT16_MAX,searchYMax=INT16_MAX;
    list* nodeList= (list *)(malloc(sizeof(list)));
    //nodeList->node->x=0;
    //nodeList->next=nullptr;
    for(int i=0;i<HEIGHT;i++){
        for(int j=0;j<WIDTH;j++){
            if(ChessBoard[i][j]==BLANK&&searchXMin<j){
                searchXMin=j;
            }
            if(ChessBoard[i][j]==BLANK&&searchXMax>j){
                searchXMax=j;
            }
            if(ChessBoard[i][j]==BLANK&&searchYMin<i){
                searchYMin=i;
            }
            if(ChessBoard[i][j]==BLANK&&searchYMax>i){
                searchYMax=i;
            }
        }
    }
    for(int i=searchYMin-1;i<=searchYMax;i++){
        for(int j=searchXMin-1;j<=searchXMax;j++) {
            if(ChessBoard[i][j]==BLANK){
                createNode(nodeList,createPoint(j,i));
            }
        }
    }
    return nodeList;
}

list* updateInfo(int ChessBoard[HEIGHT][WIDTH], point* node, int depth) {
    if (node != nullptr) {
            ChessBoard[node->y][node->x] = whoIsPlay(depth);
    }
    return searchPoint(ChessBoard);
}


tree* createAdjTreeNode(tree* B, point* node){
    tree* temp= (tree *)(malloc(sizeof(tree)));
    temp->node=node;
    temp->value=0;
    temp->next=nullptr;
    B->adj=temp;
    return temp;
}

tree* createNextTreeNode(tree* B, point* node){
    tree* temp= (tree *)(malloc(sizeof(tree)));
    temp->node=node;
    temp->value=0;
    temp->adj=nullptr;
    B->next=temp;
    return temp;
}

void createTree(int ChessBoard[HEIGHT][WIDTH], list *nodeList, tree *treeNode, int depth){
    if(depth<=DEPTH){
        tree* treeAdj;
        if(nodeList!= nullptr){
            treeAdj=createAdjTreeNode(treeNode,nodeList->node);
            createTree(ChessBoard,nodeList->next,treeNode->adj,depth);
        }
        tree* treeNext;
        if(treeNode!= nullptr){
            list* temp=updateInfo(ChessBoard,treeNode->node,++depth);
            treeNext=createNextTreeNode(treeAdj,temp->node);
            createTree(ChessBoard,temp,treeNext->adj,depth);
        }
    }
}

int valuePoint(int ChessBoard[HEIGHT][WIDTH], stack* bottom){
    //TODO: Chen Lu's work
    return 0;
}

void valueLeafNode(int ChessBoard[HEIGHT][WIDTH], tree* treeRoot, stack* bottom){
    if(treeRoot->next!= nullptr){
        push(bottom,treeRoot->node);
        valueLeafNode(ChessBoard,treeRoot->next,bottom);
    }
    if(treeRoot->adj!= nullptr){
        push(bottom,treeRoot->node);
        treeRoot->value=valuePoint(ChessBoard,bottom);
        pop(bottom);
        valueLeafNode(ChessBoard,treeRoot->adj,bottom);
    }
}

int minAdjNode(tree* treeNode){
    int min=INT16_MAX;
    if(min>treeNode->value){
        minAdjNode(treeNode->adj);
    }
    return min;
}

int maxAdjNode(tree* treeNode){
    int max=INT16_MAX;
    if(max>treeNode->value){
        maxAdjNode(treeNode->adj);
    }
    return max;
}

int AlphaBetaPure(tree* treeRoot, int depth){
    if(treeRoot->next->next!= nullptr){
        AlphaBetaPure(treeRoot->next,depth+1);
    }
    if(treeRoot->adj!= nullptr){
        if(whoIsPlay(depth)==BLACK){
            treeRoot->value=minAdjNode(treeRoot->next);
        }else{
            treeRoot->value=maxAdjNode(treeRoot->next);
        }
        AlphaBetaPure(treeRoot->adj,depth);
    }
    return treeRoot->value;
}

point* playGame(int ChessBoard[HEIGHT][WIDTH], int hands){
    srand(time(nullptr));
    if(hands==0){
        auto* randomPoint=(point*)malloc(sizeof(point));
        randomPoint->x=rand()%5+5;
        randomPoint->y=rand()%5+5;
        return randomPoint;
    }
    tree* treeRoot = (tree *)(malloc(sizeof(tree)));
    createTree(ChessBoard,searchPoint(ChessBoard),treeRoot,0);
    int result=AlphaBetaPure(treeRoot,0);
    tree* p=treeRoot;
    for(;p!= nullptr;p=p->adj){
        if(p->value==result){
            break;
        }
    }
    return p->node;
}

int valueChessBoard(int ChessBoard[HEIGHT][WIDTH]){
    return 0;
}

int isWin(int ChessBoard[HEIGHT][WIDTH]){
    int result=valueChessBoard(ChessBoard);
    switch (result) {
        case 1:
            return WIN;
        case 2:
            return LOSE;
        case 3:
            return TIE;
        default:
            return UNSETTLED;
    }
}

int main() {
    int ChessBoard[HEIGHT][WIDTH];
    for(auto & i : ChessBoard){
        for(int & j : i){
            j=BLANK;
        }
    }
    int hands=0;
    int ChessStatus=UNSETTLED;
    while(ChessStatus==UNSETTLED){
        point* result=playGame(ChessBoard,hands);
        printf("%d,%d\n",result->x,result->y);
        ChessBoard[result->y][result->x]=whoIsPlay(hands);
        hands++;
        int x,y;
        scanf_s("%d,%d",&x,&y);
        ChessBoard[y][x]=whoIsPlay(hands);
        hands++;
        ChessStatus=isWin(ChessBoard);
    }
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
