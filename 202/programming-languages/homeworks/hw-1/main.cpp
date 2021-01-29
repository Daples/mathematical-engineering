  #include <iostream>
//#include "nada.cpp"
using namespace std;

class Nodo {
  private:
     int dato;
     Nodo *sig;

  friend class Lista;
  public:
     Nodo (int dato, Nodo *sig=NULL);
     ~Nodo(){}
};

Nodo::Nodo(int dato, Nodo *sig){
  this->dato = dato;
  this->sig = sig;
}

typedef Nodo *apNodo;  //typedef int numerito;


class Lista {
  public:
    Lista(){
      this->cab = NULL;
    }
    ~Lista(){}

    //Funciones con la Lista
    void mostrarLista();

    //adicionar
    void adicionar(apNodo elemento);
    void adicionar(int valor);
    void adicionarCola(apNodo elemento);
    void adicionarCola(int valor);
    void adicionarOrdenado(apNodo elemento);
    void adicionarOrdenado_old(apNodo elemento);
    void adicionarOrdenado(int valor);

    // Tareas
    //tamaño
    int length();

    //quitarElemento
    bool quitar(apNodo elemento);
    bool quitar(int elemento);
    void quitarTodos(apNodo elemento);

    //buscarElemento
    bool search(apNodo elemento);
    bool search(int elemento);

    //invertir
    void reverse();

  private:
    apNodo cab;
};

/* ========== Funciones dadas por el profesor ========== */
/* Adicionar orderando método viejo*/
void Lista::adicionarOrdenado_old(apNodo elemento){
  if (!this->cab)
    this->cab = elemento;
  else {
    if (this->cab->dato > elemento->dato){
      elemento->sig = this->cab;
      this->cab = elemento;
    }
    else {
        apNodo item = this->cab;
        while (item->sig != NULL){
          if (elemento->dato > item->sig->dato){
            item = item->sig;
          }
          else{
            break;
          }
        }
        elemento->sig = item->sig;
        item->sig = elemento;
    }
  }
}

/* Adicionar ordenado para un nodo */
void Lista::adicionarOrdenado(apNodo elemento){
  if (!this->cab) {
    this->cab = elemento;
  }
  else {
    if (this->cab->dato <= elemento->dato){
      elemento->sig = this->cab;
      this->cab = elemento;
    }
    else {
        apNodo item = this->cab;
        while ((item->sig != NULL)&&(elemento->dato <= item->sig->dato)){
          item = item->sig;
        }
        elemento->sig = item->sig;
        item->sig = elemento;
    }
  }
}

/* Adicionar ordenado para un valor */
void Lista::adicionarOrdenado(int valor){
   adicionarOrdenado(new Nodo(valor));
}

/* Adicionar un nodo al comienzo de la lista */
void Lista::adicionar(apNodo elemento){
  elemento->sig = this->cab;
  this->cab = elemento;
}

/* Adicionar un valor al comienzo de la  lista */
void Lista::adicionar(int valor){
  this->cab = new Nodo(valor, this->cab);
}

/* Adicionar al final de la lista */
void Lista::adicionarCola(apNodo elemento){
  if (!this->cab){
    this->cab = elemento;
  } else {
    apNodo item = this->cab;
    apNodo sig = item->sig;
    while (sig){
      item = item->sig;
      sig = item->sig;
    }
    item->sig = elemento;
  }
}

void Lista::adicionarCola(int valor){
  adicionarCola(new Nodo(valor));
}

/* Función para imprimir la lista */
void Lista::mostrarLista(){
  apNodo item = this->cab;
  while (item){
    cout << "["<< item->dato <<"]->";
    item=item->sig;
  };
  cout << "NULL" << endl;
}

/* ========== Pruebas ========== */
void prueba(){
  Lista *lista = new Lista();

  apNodo nodo = new Nodo(3);
  lista->adicionarCola(nodo);

  nodo = new Nodo(13);
  lista->adicionarCola(nodo);

  lista->adicionarCola(new Nodo(21));
  lista->adicionarCola(54);

  lista->mostrarLista();
}

void prueba2(){

  Lista *lista = new Lista();
  lista->adicionarOrdenado(5);
  lista->adicionarOrdenado(2);
  lista->adicionarOrdenado(9);
  lista->adicionarOrdenado(6);
  lista->adicionarOrdenado(2);
  lista->adicionarOrdenado(9);
  lista->adicionarOrdenado(35);

  lista->mostrarLista();
  lista -> reverse();
  lista -> mostrarLista();
}

/* ========== Tareas ========== */
// Longitud de la lista
int Lista::length() {
  if (!this -> cab) {
    return 0;
  }
  int size = 0;
  apNodo item = this->cab;
  while (item){
    item = item->sig;
    size += 1;
  }
  return size;
}

// Quita la primera ocurrencia de un nodo
bool Lista::quitar(apNodo elemento) {
  if (this -> cab -> dato == elemento -> dato) {
    this -> cab = this -> cab -> sig;
  }

  apNodo item = this -> cab;
  apNodo sig = item -> sig;
  while (sig) {
    if (sig -> dato == elemento -> dato) {
      item -> sig = sig -> sig;
      return true;
    }
    item = item -> sig;
    sig = item -> sig;
  }
  return false;
}

// Quitar la primera ocurrencia de un elemento
bool Lista::quitar(int elemento) {
  return quitar(new Nodo(elemento));
}

// Se eliminan todas las repeticiones de un nodo
void Lista::quitarTodos(apNodo elemento) {
  if (this -> cab -> dato == elemento -> dato) {
    this -> cab = this -> cab -> sig;
  }

  apNodo item = this -> cab;
  apNodo sig = item -> sig;
  while (sig) {
    if (sig -> dato == elemento -> dato) {
      item -> sig = sig -> sig;
      sig = item -> sig;
    }
    else {
      item = item -> sig;
      sig = item -> sig;
    }
  }
}

// Busca si un nodo está en la lista
bool Lista::search(apNodo elemento) {
  if (!this -> cab) {
    return false;
  }
  int size = 0;
  apNodo item = this->cab;
  while (item){
    item = item->sig;
    size += 1;
  }
  return size;
}

// Busca si un entero está en la lista
bool Lista::search(int elemento) {
  return search(new Nodo(elemento));
}

// Reversa la lista
void Lista::reverse() {
  if (!this -> cab)
    return;

  apNodo sig = this -> cab -> sig;
  this -> cab -> sig = NULL;
  apNodo item = this -> cab;
  while (sig) {
    apNodo sigAux = sig -> sig;
    sig -> sig = item;
    item = sig;
    sig = sigAux;
  }
  this -> cab = item;
}

int main() {
  prueba2();
}
