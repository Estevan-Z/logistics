
from django.shortcuts import get_object_or_404, render, redirect
from .models import Producto, ParametrosProducto, Proveedor, EntradaMercancia
from django.core.files.storage import default_storage
from .forms import ProductoForm, ProveedorForm
from django.http import JsonResponse
from django.contrib import messages
import pandas as pd
import openpyxl
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import json

def base(request):
    return render(request, 'Home/base.html')

def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_proveedores')  
    else:
        form = ProveedorForm()
    return render(request, 'Proveedor/crear_proveedores.html', {'form': form})


def lista_proveedores(request):
    proveedores = Proveedor.objects.values(
        'id_proveedor',
        'nombre_comercial',
        'representante_legal',
        'nit',
        'direccion',
        'telefono',
        'correo_electronico'
    )
    
    return render(request, 'Proveedor/Lista_proveedores.html', {'proveedores': proveedores})

def parametros_producto(request):
    if request.method == "POST":
        grupo = request.POST.get("grupo")
        linea = request.POST.get("linea")
        unidad = request.POST.get("unidad")

        if "guardar_grupo" in request.POST and grupo:
            ParametrosProducto.objects.create(grupo=grupo)
        if "guardar_linea" in request.POST and linea:
            ParametrosProducto.objects.create(linea=linea)
        if "guardar_unidad" in request.POST and unidad:
            ParametrosProducto.objects.create(unidad=unidad)

        return redirect('parametros_producto')  

    return render(request, 'Parametros/Crear_parametros.html')



def listar_parametros(request):
    parametros = ParametrosProducto.objects.all()
    return render(request, 'Parametros/listar_parametros.html', {'parametros': parametros})


def eliminar_parametro(request, parametro_id):
    parametro = get_object_or_404(ParametrosProducto, id=parametro_id)
    parametro.delete()
    return redirect('listar_parametros')


def editar_parametro(request, parametro_id):
    parametro = get_object_or_404(ParametrosProducto, id=parametro_id)

    if request.method == 'POST':
        nuevo_valor = request.POST.get('nuevo_valor')
        if nuevo_valor:
            if parametro.grupo:
                parametro.grupo = nuevo_valor
            elif parametro.linea:
                parametro.linea = nuevo_valor
            elif parametro.unidad:
                parametro.unidad = nuevo_valor
            parametro.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': 'El valor no puede estar vacío.'}, status=400)
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'Parametros/editar_parametro_form.html', {'parametro': parametro})
        else:
            return render(request, 'Parametros/editar_parametro.html', {'parametro': parametro})

def crear_producto(request):
    if request.method == 'POST':
        archivo_excel = request.FILES.get('archivo_excel')
        
        if archivo_excel:
            ruta_archivo = default_storage.save(archivo_excel.name, archivo_excel)
            ruta_completa = default_storage.path(ruta_archivo)

            try:
                wb = openpyxl.load_workbook(ruta_completa)
                hoja = wb.active

                for fila in hoja.iter_rows(min_row=2, values_only=True):  
                    nombre_producto, marca, grupo, linea, unidad = fila

                    parametros, _ = ParametrosProducto.objects.get_or_create(
                        grupo=grupo, linea=linea, unidad=unidad
                    )

                    Producto.objects.create(
                        nombre_producto=nombre_producto,
                        marca=marca,
                        grupo=parametros.grupo,
                        linea=parametros.linea,
                        unidad=parametros.unidad,
                    )
                wb.close()
                default_storage.delete(ruta_archivo)
                return redirect('listar_productos')
            except Exception as e:
                print(f"Error al procesar el archivo Excel: {e}")
        
        else:
            form = ProductoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('listar_productos')

    else:
        form = ProductoForm()

    return render(request, 'Productos/Crear_producto.html', {'form': form})


def listar_productos(request):
    productos = Producto.objects.all()
    parametros = ParametrosProducto.objects.all()
    return render(request, 'Productos/Listar_productos.html', {'productos': productos, 'parametros': parametros})

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})  
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = ProductoForm(instance=producto)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'Productos/Editar_producto.html', {'form': form})
        else:
            return render(request, 'Productos/Editar_producto.html', {'form': form, 'producto': producto})



def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    producto.delete()
    return redirect('listar_productos')


def subir_excel(request):
    if request.method == 'POST':
        archivo_excel = request.FILES['archivo_excel']
        
        try:

            data = pd.read_excel(archivo_excel)

            for index, row in data.iterrows():
                grupo, linea, unidad = row['grupo'], row['linea'], row['unidad']

                if grupo and not ParametrosProducto.objects.filter(grupo=grupo).exists():
                    ParametrosProducto.objects.create(grupo=grupo)
                if linea and not ParametrosProducto.objects.filter(linea=linea).exists():
                    ParametrosProducto.objects.create(linea=linea)
                if unidad and not ParametrosProducto.objects.filter(unidad=unidad).exists():
                    ParametrosProducto.objects.create(unidad=unidad)

                Producto.objects.create(
                    nombre_producto=row['nombre_producto'],
                    marca=row['marca'],
                    grupo=grupo,
                    linea=linea,
                    unidad=unidad
                )

            messages.success(request, "Productos cargados exitosamente desde el Excel.")
        except Exception as e:
            messages.error(request, f"Error al procesar el archivo Excel: {e}")

        return redirect('crear_producto') 
    return render(request, 'Productos/Crear_producto.html')



def editar_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)
    
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = ProveedorForm(instance=proveedor)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'Proveedor/editar_proveedor_form.html', {'form': form})
        else:
            return render(request, 'Proveedor/editar_proveedor.html', {'form': form})

def eliminar_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)
    proveedor.delete()
    return redirect('lista_proveedores')  




def registrar_entrada(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        producto_id = request.POST.get('producto')
        lote = request.POST.get('lote')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        cantidad = request.POST.get('cantidad')
        observaciones = request.POST.get('observaciones')

        if not proveedor_id or not producto_id or not cantidad:
            error = "Por favor, completa todos los campos obligatorios."
            proveedores = Proveedor.objects.all()
            productos = Producto.objects.all()
            return render(request, 'Entradas/Nota_Entrada.html', {
                'proveedores': proveedores,
                'productos': productos,
                'error': error,
            })

        EntradaMercancia.objects.create(
            proveedor_id=proveedor_id,
            producto_id=producto_id,
            lote=lote,
            fecha_vencimiento=fecha_vencimiento if fecha_vencimiento else None,
            cantidad=cantidad,
            observaciones=observaciones
        )
        return redirect('listar_entradas')  
    proveedores = Proveedor.objects.all()
    productos = Producto.objects.all()
    return render(request, 'Entradas/Nota_Entrada.html', {
        'proveedores': proveedores,
        'productos': productos,
    })



def Vista_Entradapdf(request):
    return render(request, 'Entradas/Vista_Entradapdf.html')

def guardar_entrada(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        proveedor_id = data.get('proveedor_id')
        observacion = data.get('observacion')
        productos = data.get('productos')

        # Crear nueva entrada con ID automático
        nueva_entrada = EntradaProducto(proveedor_id=proveedor_id, observacion=observacion)
        nueva_entrada.save()  # Se genera automáticamente el id_entrada

        # Aquí puedes guardar los productos asociados si tienes un modelo relacionado

        return JsonResponse({"mensaje": "Entrada guardada correctamente", "id_entrada": nueva_entrada.id_entrada})

    return JsonResponse({"error": "Método no permitido"}, status=400)
