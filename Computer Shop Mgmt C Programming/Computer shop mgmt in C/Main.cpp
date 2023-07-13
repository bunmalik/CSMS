// txt files are not available

#include<stdio.h>
#include<conio.h>
#include<stdlib.h>
#include<string.h>
#include<windows.h>
#define ERROR puts("\n=================\n|\a   ERROR!	|\n=================")
//display tags functions
void TITLE();
int comptag(int);
void CUSTOMERPANEL();
void ADMINPANEL();
int pcpur(int);
//PC Purchase function
int PCPurchase();
//Admin database
void Adminpermit();

FILE *fptr;
//Password verifier
int Access();
//Adminpermit functions
void Add();
void Modify();
void Delete();
void Search();
void View();
//global structure declaration
struct pc {
	char laptopcompany[100];
	char RAM[100];
	char Processor[100];
	int price;
} PC;
int addition=1;
//start of program
main(){
	int choice; int acc;
	TITLE();
	comptag(0);
	system("color 0");
	puts("\tWhat would you like to do?");
	puts("	1. Wish to purchase computer components as a customer:");
	puts("	2. Login as Authorized Administrator");
	puts("	3. Exit");
	puts("Enter a choice:");
	scanf("%d",&choice);
	switch (choice){
		case 1 : { PCPurchase(); break;}
		case 2 : { system("color 4E"); acc=Access(); if(acc==1) Adminpermit(); else {getch(); main();}}
		default : { comptag(0); system("color B1"); puts("\n\n\n\n\n\n\t\t\t\tTHANK YOU"); puts("\n\t\tFOR CHOOSING LUMINOUS DIODE SOLUTIONS"); fclose(fptr); getch(); exit(0);}
	}
}
void Adminpermit(){
	system("color 0");
	int choice1;
	fptr=fopen("laptopdatabase.txt","ab+");
	fseek(fptr,0,0);
	comptag(0);
	ADMINPANEL();
	printf("1. Add new laptop stock");
	printf("\n2. View available stock");
	printf("\n3. Modify existing laptop models");
	printf("\n4. Search for an exsiting laptop model");
	printf("\n5. Delete models out of stock");
	printf("\n6. Return to previous screen\n");
	printf("Enter a choice: ");
	scanf("%d",&choice1);
	switch (choice1){
		case 1 : Add();
		case 2 : View();
		case 3 : Modify();
		case 4 : Search();
		case 5 : Delete();
		case 6 : main();
	}
}
void Add()
{	
	int offset;
	comptag(0); char id[100];
	ADMINPANEL();
	printf("\n\t\t     ***** Current Selection: Addition of new stock *****");
		fflush(stdin);
		printf("\nLaptop company and name: ");
		gets(id);
		while(fread(&PC,sizeof(PC),1,fptr)==1){
		if((strcmpi(PC.laptopcompany,id))==0)
		{	ERROR;
			printf("\nSorry. This model already exists.\n");
			printf("\nPress any key to start adding another model...\n");
			getch();
			Add();
		}
		}
		strcpy(PC.laptopcompany,id);
		printf("RAM: ");
		gets(PC.RAM);
		printf("Processor: ");
		gets(PC.Processor);
		printf("Price: ");
		scanf("%d",&PC.price);
		//offset=(addition-1)*sizeof(PC);
		//fseek(fptr,offset,0);
		fwrite(&PC,sizeof(PC),1,fptr);
		//addition++;
		printf("\nPress any key to return to previous menu...\n");
		getch();
		//if(addmore=='Y' || addmore=='y') {fclose(fptr); Add();}
		//else {
		fclose(fptr);
		Adminpermit();
		}
void View()
{	comptag(0);
	ADMINPANEL();
	printf("\n\t\t     ***** Current Selection: Viewing available stock *****");
	rewind(fptr);
	while(fread(&PC,sizeof(PC),1,fptr)==1)
	{	printf("\n\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
		printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
		printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
		printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
		printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
		printf("\nLaptop company and name: ");
		puts(PC.laptopcompany);
		printf("RAM: ");
		puts(PC.RAM);
		printf("Processor: ");
		puts(PC.Processor);
		printf("Price: ");
		printf("%d",PC.price);
	}
	printf("\nPress any key to continue to previous menu...");
	getch();
	system("cls");
	fclose(fptr);
	Adminpermit();
}

void Modify()
{	fflush(stdin);
	comptag(0);
	ADMINPANEL();
	FILE *tptr;
	printf("\n\t\t     ***** Current selection: Modification of existing laptop models *****");
	char id[30]; int a=0;
	char another='y';
	while(another=='y' || another=='Y')
	{	fflush(stdin);
		printf("\nEnter laptop company and name to modify: ");
		gets(id);
		tptr=fopen("temporary.txt","wb");
		rewind(fptr);
		int flag=0, flag1=0, flag2;
		while(fread(&PC,sizeof(PC),1,fptr)==1)
		{	
			if(strcmpi(PC.laptopcompany,id)==0)
			{	flag1++; flag2=1;
				fflush(stdin);
				printf("\"%s\" exists in database!\n",id); flag=10;
				printf("New laptop company and name: ");
				gets(PC.laptopcompany);
				printf("New RAM Capacity: ");
				gets(PC.RAM);
				printf("New Processor: ");
				gets(PC.Processor);
				printf("Price: ");
				scanf("%d",&PC.price);
				if(flag1==1 && flag2==1) {fseek(tptr,0,0);}	
				else { fseek(tptr,(flag1-1)*sizeof(PC),0);}
				fwrite(&PC,sizeof(PC),1,tptr);
			}
			else
			{ flag1++;	fwrite(&PC,sizeof(PC),1,tptr); }
			
		}
		if(flag!=10){ ERROR; puts("No such record exists!");}
		fclose(fptr);
		fclose(tptr);
		remove("laptopdatabase.txt");
		rename("temporary.txt","laptopdatabase.txt");
		fptr=fopen("laptopdatabase.txt","ab+");
		printf("\nModify another laptop? (Y/N)? ");
		fflush(stdin);
		another = getche();
	}
	fclose(fptr);
	Adminpermit();
}
void Search()
{	int a=0; char id[30];
	comptag(0);
	ADMINPANEL();
	fptr=fopen("laptopdatabase.txt","ab+");
	fflush(stdin);
	printf("\n\t\t     ***** Current Selection: Search in available stock *****");
	puts("\nEnter laptop name and company to search: ");
	gets(id);
	while(fread(&PC,sizeof(PC),1,fptr)==1)
	{	if(strcmpi(PC.laptopcompany,id)==0){
		puts("\n-------------------------------------------------\n\t\t SEARCH QUERY MATCHED:\n-------------------------------------------------\n");
		printf("\nLaptop company and name: ");
		puts(PC.laptopcompany);
		printf("RAM: ");
		puts(PC.RAM);
		printf("Processor: ");
		puts(PC.Processor);
		printf("Price: ");
		printf("%d",PC.price); a=1;}
	}
	if (a!=1) {	ERROR; printf("\n%s doesn't exist in the database!\n",id);}
	printf("\nPress any key to continue to previous menu...");
	getch();
	system("cls");
	fclose(fptr);
	Adminpermit();
}
void Delete()
{	fflush(stdin);
	comptag(0);
	ADMINPANEL();
	FILE *tptr;
	printf("\n\t\t     ***** Current selection: Deletion of existing laptop models that are out of stock *****");
	char id[30]; int a=0;
	char another='y';
	while(another=='y' || another=='Y')
	{	fflush(stdin);
		printf("\nEnter laptop company and name to delete: ");
		gets(id);
		tptr=fopen("tempdel.txt","wb");
		rewind(fptr);
		int flag=0;
		while(fread(&PC,sizeof(PC),1,fptr)==1)
		{
			
			if(strcmpi(PC.laptopcompany,id)!=0)
			{	
				fwrite(&PC,sizeof(PC),1,tptr);
			}
			else if(strcmpi(PC.laptopcompany,id)==0){
			puts("\a\nLaptop delete successful!\n");
			 flag=10; }
		}
		if(flag!=10){ ERROR; puts("No such record exists!");}
		fclose(fptr);
		fclose(tptr);
		remove("laptopdatabase.txt");
		rename("tempdel.txt","laptopdatabase.txt");
		fptr=fopen("laptopdatabase.txt","ab+");
		printf("\nDelete another model out of stock? (Y/N)? ");
		fflush(stdin);
		another = getch();
	}
	fclose(fptr);
	Adminpermit();
}
void TITLE(){
	system("cls");
	system("color 0");
	printf("\n\n\n\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\nBROUGHT TO YOU BY:\n\n\nCODE-PROJECTS \ncode-projects.org\n");
	//printf("\n\n\n\t\t\tGeekACode.com\n");
	//printf("\n\n\n\t Provider of the best computer components\n\n\n");
	
	printf("\n\n\n\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\n");
	puts("\nPress any key to continue");
	getch();
}
int comptag(int bal){
	system("cls");
	printf("\n=================================================================================================================\n");
	printf("\n\t\tLUMINOUS DIODE SOLUTIONS(R)\n");
	printf("\t Provider of the best computer components\n");
	printf("\n=================================================================================================================\n");
}
int pcpur(int bal){
	system("cls");
	printf("\n=================================================================================================================\n");
	printf("\n\t\tLUMINOUS DIODE SOLUTIONS(R)\n");
	printf("\t Provider of the best computer components\n"); printf("\n\t\t\t\t\t\tCurrent expense = %d",bal);
	printf("\n=================================================================================================================\n");
}
int Access(){
	fflush(stdin);
	char admin[30]; static char password[5]; int a;
	printf("\n\t\t\tEnter Admin username: ");
	scanf("%s",&admin);
	if(strcmpi(admin,"code-projects")==0 || strcmpi(admin,"xyz")==0 || strcmpi(admin,"abc")==0)
	{ puts("\n\n\t\t\tAdmin identity verified!");
	printf("\n\t\t\tEnter 5-digit database password: \n\t\t\t ");
	for(int i=0;i<5;i++){
	password[i]=getch();
	if(password[i]=='\r') {break;}
	else
	printf("*");
						}
	if(strcmp(password,"12345")==0){
		puts("\a\n\n\n\t\t\tACCESS GRANTED"); getch(); a=1;}
	else{
	puts("\a\n\n\n\t\t\tACCESS DENIED!"); a=0;}
	}
	else { comptag(0); puts("\n\n\n\t\t\tUNKNOWN IDENTITY"); a=0;} 
	return a;
}
int PCPurchase()
{	system("color 0");
	comptag(0); char laptop[100];
	CUSTOMERPANEL();
	fptr=fopen("laptopdatabase.txt","ab+");
	puts("Available laptops: \n\n");
	rewind(fptr);
	while(fread(&PC,sizeof(PC),1,fptr)==1)
	{
		printf("\nLaptop company and name: ");
		puts(PC.laptopcompany);
		printf("RAM: ");
		puts(PC.RAM);
		printf("Processor: ");
		puts(PC.Processor);
		printf("Price: ");
		printf("%d",PC.price);
	}
	puts("\n\nPress any key to continue purchase");
	getch();
	comptag(0);
	fflush(stdin);
	puts("Enter the laptop company and name you want to buy: \n(Type 'RETURN' if you do not want to purchase)");
	gets(laptop);
	comptag(0);
	rewind(fptr);
	while(fread(&PC,sizeof(PC),1,fptr)==1)
	{	if(strcmpi(PC.laptopcompany,laptop)==0){
		pcpur(PC.price);
		puts("\n-------------------------------------------------\n\t\t YOU SELECTED:\n-------------------------------------------------\n");
		printf("\nLaptop company and name: ");
		puts(PC.laptopcompany);
		printf("RAM: ");
		puts(PC.RAM);
		printf("Processor: ");
		puts(PC.Processor);
		printf("Price: ");
		printf("%d",PC.price);
		printf("\n\n\t\t\tYOUR TOTAL BILL: %d",PC.price);
		printf("\nPress \"1\" to return to main screen, \"2\" to quit the program! ");
		char afterpurchase;
		afterpurchase=getche();
		if (afterpurchase=='1'){ fclose(fptr); main();}
		else { comptag(0); system("color B1"); puts("\n\n\n\n\n\n\t\t\t\tTHANK YOU"); puts("\n\t\tFOR CHOOSING LUMINOUS DIODE SOLUTIONS"); fclose(fptr); getch(); exit(0);}
			}
		else if(strcmpi("RETURN",laptop)==0) {main(); }
		else { puts("\nNot available!\n Press any key to continue!"); getch(); PCPurchase();}
		}		
	}
void ADMINPANEL(){
	printf("\t");
		printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\n\t\t\t\t\tADMIN PANEL\n");
	printf("\t");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\n");
}
void CUSTOMERPANEL(){
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\n\t\t\tCUSTOMER PURCHASE\n");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD");
	printf("\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\xCD\n");
}
