from django.core.management.base import BaseCommand
from outflows.models import Outflow
from products.models import Product
from suppliers.models import Supplier
import csv


class Command(BaseCommand):
    help = 'Importa dados de Outflow a partir de um arquivo CSV, buscando produto de forma case-insensitive.'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help='Nome do arquivo CSV com outflows',
        )

    def handle(self, *args, **options):
        file_name = options['file_name']
        
        with open(file_name, 'r', encoding='utf-8-sig') as file:
            # Ajuste o 'delimiter' conforme necessário (',' ou ';')
            reader = csv.DictReader(file, delimiter=';')
            
            for row in reader:
                produto_original = row['produto']  # valor que vem cru do CSV
                
                descricao = row['descricao']
                quantidade = int(row['quantidade'])

                # Remove espaços extras no início e final
                produto_limpo = produto_original.strip()
                
                # Tenta primeiro buscar de forma exata, mas ignorando maiúsculo/minúsculo
                product_obj = Product.objects.filter(title__iexact=produto_limpo).first()

                if not product_obj:
                    # Se não encontrar, tenta achar um "aproximado" (que contenha a string)
                    product_obj = Product.objects.filter(title__icontains=produto_limpo).first()

                if not product_obj:
                    self.stdout.write(self.style.ERROR(
                        f'Produto "{produto_original}" não encontrado. Verifique seu CSV.'
                    ))
                    continue
                
                

                # Cria o Outflow
                outflow = Outflow.objects.create(
                    product=product_obj,
                    
                    quantity=quantidade,
                    description=descricao
                )

                self.stdout.write(self.style.NOTICE(
                    f'outflow criado com sucesso: {outflow.product} ({outflow.quantity})'
                ))
        
        self.stdout.write(self.style.SUCCESS(
            'Importação de outflows concluída com sucesso!'
        ))
