<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Device;
use Illuminate\Http\JsonResponse;

class DeviceController extends Controller
{
    public function get(): JsonResponse
    {
        $devices = Device::all();

        $groupedData = [];

        foreach ($devices as $item) {
            $group = $item["group"];
            unset($item["group"]);
            $groupedData[$group][] = $item;
        }

        return response()->json($groupedData);
    }

    public function store(): JsonResponse
    {

        $validated = request()->validate([
            'name' => ['required', 'string'],
            'memory' => ['required', 'string'],
            'model' => ['required', 'string'],
            'group' => ['required', 'string'],
            'price' =>['required', 'numeric']
        ]);

        $name = $validated['name'];
        $price = $validated['price'];
        $memory = $validated['memory'];
        $model = $validated['model'];
        $group = $validated['group'];

        $item = [
            'price' => $price,
            'name' => $name,
            'memory'=> $memory,
            'model'=>$model,
            'group'=>$group
        ];


        Device::create($item);

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

        foreach ($decodedData as $device) {
            $price = empty($device['price']) ? 0 : $device['price'] ;
            $name = empty($device['name']) ? ' ': $device['name'];
            $memory = empty($device['memory']) ? ' ': $device['memory'];
            $model = empty($device['model']) ? ' ': $device['model'];
            $group = empty($device['group']) ? ' ': $device['group'];

            $item = [
                'price' => $price,
                'name' => $name,
                'memory'=> $memory,
                'model'=>$model,
                'group'=>$group
            ];


            Device::create($item);
        }

        return response()->json([
            'message' => 'success'
        ]);
    }
}
