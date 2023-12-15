<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Phone;
use Illuminate\Http\JsonResponse;

class PhoneController extends Controller
{
    public function get()
    {
        $phones = Phone::all();

        return $phones->map(function($phone, $key) {
            return [
                'price' => $phone->price,
                'name' => $phone->name,
                'memory'=> $phone->memory,
                'model'=>$phone->model
            ];
        });
    }

    public function store(): JsonResponse
    {

        $validated = request()->validate([
            'name' => ['required', 'string'],
            'memory' => ['required', 'string'],
            'model' => ['required', 'string'],
            'price' =>['required', 'numeric']
        ]);

        $phoneName = $validated['name'];
        $phoneMemory = $validated['memory'];
        $phoneModel = $validated['model'];
        $phonePrice = $validated['price'];

        $item = [
            'name'=>$phoneName,
            'price'=>$phonePrice,
            'model'=>$phoneModel,
            'memory'=>$phoneMemory,
        ];


        Phone::create($item);

        return response()->json([
        'message' => 'success'
        ]);
    }

    public function storeFromRaw(): JsonResponse
    {
        $rawData = file_get_contents("php://input");
        $decodedData = json_decode($rawData, true);

        if (empty($decodedData)) {
            return response()->json(['error' => ''], 400);
        }

        foreach ($decodedData as $phone) {
            $price = $phone['price'];
            $name = $phone['name'];
            $memory = $phone['memory'];
            $model = $phone['model'];

            $item = [
                'price' => $price,
                'name' => $name,
                'memory'=> $memory,
                'model'=>$model
            ];


            Phone::create($item);
        }

        return response()->json([
            'message' => 'success'
        ]);
    }
}
