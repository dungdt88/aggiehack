<?php

namespace Csg\RouteFinderBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Csg\RouteFinderBundle\Service\RouteFinder;

/**
 * Class DefaultController
 * @package Csg\RouteFinderBundle\Command
 */
class DefaultController extends Controller
{
    /**
     * @return \Symfony\Component\HttpFoundation\Response
     */
    public function indexAction()
    {
        $finderClient = $this->get('csg_data.service.finder_client');
        die;
        
        return $this->render('CsgRouteFinderBundle:Default:index.html.twig');
    }

    /**
     * @return Response
     */
    public function ajaxCalculateRouteAction()
    {
        
        /** @var $request Request */
        $request = $this->getRequest();
        /** @var $routeFinder RouteFinder */
        $routeFinder = $this->get('csg_route_finder.service.route_finder');


        

        $data = $request->request->all();
        $responseData = array();
        $responseData['error'] = true;

//        if (empty($data['from_coordinate_lat']) || empty($data['from_coordinate_lat'])
//            || empty($data['from_coordinate_lat']) || empty($data['from_coordinate_lat'])
//            || empty($data['from_coordinate_lat'])) {
//            return new JsonResponse($responseData);
//        }
//
//        $routes = $routeFinder->findRoutes(
//            $data['from_coordinate_lat'],
//            $data['from_coordinate_long'],
//            $data['to_coordinate_lat'],
//            $data['to_coordinate_long'],
//            $data['start_time']
//        );

        $routes = $routeFinder->findRoutes(10, 20, 30, 40, 50);
        
        $responseData['error'] = false;
        
        $responseData['html'] = $this->renderView('CsgRouteFinderBundle:Finder:_results.html.twig', array(
            'routes' => $routes,
        ));
        
        return new JsonResponse($responseData);
    }
}
